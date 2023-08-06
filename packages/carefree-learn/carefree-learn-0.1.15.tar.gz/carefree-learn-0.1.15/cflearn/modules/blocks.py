import math
import torch

import numpy as np
import torch.nn as nn
import torch.nn.functional as F

from abc import abstractmethod
from abc import ABCMeta
from torch import Tensor
from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Optional
from typing import NamedTuple
from torch.nn import Module
from torch.nn import ModuleList
from cftool.misc import register_core
from cftool.misc import shallow_copy_dict
from cftool.misc import LoggingMixin
from cfdata.types import np_int_type
from cfdata.types import np_float_type

from .auxiliary import *
from ..misc.toolkit import *
from ..types import tensor_tuple_type


mapping_dict: Dict[str, Type["MappingBase"]] = {}


class Linear(Module):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        *,
        bias: bool = True,
        pruner_config: Optional[Dict[str, Any]] = None,
        init_method: Optional[str] = "xavier_uniform",
        **kwargs: Any,
    ):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim, bias)
        if pruner_config is None:
            pruner = None
        else:
            pruner = Pruner(pruner_config, [out_dim, in_dim])
        self.config, self.pruner = shallow_copy_dict(kwargs), pruner
        self._use_bias, self._init_method = bias, init_method
        with torch.no_grad():
            self.reset_parameters()

    @property
    def weight(self) -> Tensor:
        return self.linear.weight

    @property
    def bias(self) -> Optional[Tensor]:
        return self.linear.bias

    def forward(self, net: Tensor) -> Tensor:
        weight = self.linear.weight
        if self.pruner is not None:
            weight = self.pruner(weight)
        return F.linear(net, weight, self.linear.bias)

    def reset_parameters(self) -> None:
        if self._init_method is None:
            return
        if self._init_method not in Initializer.defined_initialization:
            return
        initializer = Initializer(self.config.setdefault("initialize_config", {}))
        assert isinstance(self.linear.weight, nn.Parameter)
        initializer.initialize(self.linear.weight, self._init_method)
        bias_fill = self.config.setdefault("bias_fill", 0.0)
        if self._use_bias:
            self.linear.bias.data.fill_(bias_fill)


class MappingBase(Module):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__()

    @classmethod
    def register(cls, name: str) -> Callable[[Type], Type]:
        global mapping_dict
        return register_core(name, mapping_dict)


@MappingBase.register("basic")
class Mapping(MappingBase):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        *,
        bias: Optional[bool] = None,
        pruner_config: Optional[dict] = None,
        dropout: float = 0.5,
        batch_norm: bool = True,
        activation: Optional[str] = "ReLU",
        init_method: str = "xavier_uniform",
        **kwargs: Any,
    ):
        super().__init__()
        self.config = shallow_copy_dict(kwargs)
        if bias is None:
            bias = not batch_norm
        self.linear = Linear(
            in_dim,
            out_dim,
            bias=bias,
            pruner_config=pruner_config,
            init_method=init_method,
            **shallow_copy_dict(kwargs),
        )
        self.bn = None if not batch_norm else BN(out_dim)
        if activation is None:
            self.activation: Optional[Module] = None
        else:
            activation_config = self.config.setdefault("activation_config", None)
            self.activation = Activations.make(activation, activation_config)
        use_dropout = 0.0 < dropout < 1.0
        self.dropout = None if not use_dropout else Dropout(dropout)

    @property
    def weight(self) -> Tensor:
        return self.linear.weight

    @property
    def bias(self) -> Optional[Tensor]:
        return self.linear.bias

    def forward(self, net: Tensor, *, reuse: bool = False) -> Tensor:
        net = self.linear(net)
        if self.bn is not None:
            net = self.bn(net)
        if self.activation is not None:
            net = self.activation(net)
        if self.dropout is not None:
            net = self.dropout(net, reuse=reuse)
        return net

    @classmethod
    def simple(
        cls,
        in_dim: int,
        out_dim: int,
        *,
        bias: bool = False,
        dropout: float = 0.0,
        batch_norm: bool = False,
        activation: Optional[str] = None,
        pruner_config: Optional[Dict[str, Any]] = None,
    ) -> "Mapping":
        if activation != "glu":
            activation_config = {}
        else:
            activation_config = {"in_dim": out_dim, "bias": bias}
        return cls(
            in_dim,
            out_dim,
            bias=bias,
            pruner_config=pruner_config,
            dropout=dropout,
            batch_norm=batch_norm,
            activation=activation,
            activation_config=activation_config,
        )


class _SkipConnectBlock(MappingBase, metaclass=ABCMeta):
    def __init__(
        self,
        in_dim: int,
        latent_dim: int,
        *,
        bias: Optional[bool] = None,
        pruner_config: Optional[dict] = None,
        dropout: float = 0.0,
        batch_norm: bool = True,
        activation: Optional[str] = "ReLU",
        init_method: str = "xavier_uniform",
        **kwargs: Any,
    ):
        super().__init__()
        self.linear_mapping = Linear(
            in_dim,
            latent_dim,
            bias=True if bias is None else bias,
            pruner_config=pruner_config,
            init_method=init_method,
            **kwargs,
        )
        self.nonlinear_mapping = Mapping(
            in_dim,
            latent_dim,
            bias=bias,
            pruner_config=pruner_config,
            dropout=dropout,
            batch_norm=batch_norm,
            activation=activation,
            init_method=init_method,
            **kwargs,
        )

    def forward(self, net: Tensor) -> Tensor:
        linear = self.linear_mapping(net)
        nonlinear = self.nonlinear_mapping(net)
        return self._skip_connect(net, linear, nonlinear)

    @abstractmethod
    def _skip_connect(self, net: Tensor, linear: Tensor, nonlinear: Tensor) -> Tensor:
        pass


@MappingBase.register("res")
class ResBlock(_SkipConnectBlock):
    def __init__(
        self,
        in_dim: int,
        latent_dim: int,
        *,
        bias: Optional[bool] = None,
        pruner_config: Optional[dict] = None,
        dropout: float = 0.0,
        batch_norm: bool = True,
        activation: Optional[str] = "ReLU",
        init_method: str = "xavier_uniform",
        **kwargs: Any,
    ):
        super().__init__(
            in_dim,
            latent_dim,
            bias=bias,
            pruner_config=pruner_config,
            dropout=dropout,
            batch_norm=batch_norm,
            activation=activation,
            init_method=init_method,
            **kwargs,
        )
        self.res_linear = Linear(
            latent_dim,
            latent_dim,
            bias=True if bias is None else bias,
            pruner_config=pruner_config,
            init_method=init_method,
            **kwargs,
        )
        self.res_bn = None if not batch_norm else BN(latent_dim)
        self.res_dropout = Dropout(dropout)
        if activation is None:
            self.res_activation: Optional[Module] = None
        else:
            activation_config = kwargs.setdefault("activation_config", None)
            self.res_activation = Activations.make(activation, activation_config)

    def _skip_connect(self, net: Tensor, linear: Tensor, nonlinear: Tensor) -> Tensor:
        net = linear + self.res_linear(nonlinear)
        if self.res_bn is not None:
            net = self.res_bn(net)
        net = self.res_dropout(net)
        if self.res_activation is None:
            return net
        return self.res_activation(net)


@MappingBase.register("highway")
class HighwayBlock(_SkipConnectBlock):
    def __init__(
        self,
        in_dim: int,
        latent_dim: int,
        *,
        bias: Optional[bool] = None,
        pruner_config: Optional[dict] = None,
        dropout: float = 0.0,
        batch_norm: bool = True,
        activation: Optional[str] = "ReLU",
        init_method: str = "xavier_uniform",
        **kwargs: Any,
    ):
        super().__init__(
            in_dim,
            latent_dim,
            bias=bias,
            pruner_config=pruner_config,
            dropout=dropout,
            batch_norm=batch_norm,
            activation=activation,
            init_method=init_method,
            **kwargs,
        )
        self.gate_linear = Linear(
            in_dim,
            latent_dim,
            bias=True if bias is None else bias,
            pruner_config=pruner_config,
            init_method=init_method,
            **kwargs,
        )
        self.sigmoid = nn.Sigmoid()

    def _skip_connect(self, net: Tensor, linear: Tensor, nonlinear: Tensor) -> Tensor:
        gate = self.sigmoid(self.gate_linear(net))
        return gate * nonlinear + (1.0 - gate) * linear


class MLP(Module):
    def __init__(
        self,
        in_dim: int,
        out_dim: Optional[int],
        num_units: List[int],
        mapping_configs: Union[Dict[str, Any], List[Dict[str, Any]]],
        *,
        mapping_type: str = "basic",
        final_mapping_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        mappings: List[Module] = []
        if isinstance(mapping_configs, dict):
            mapping_configs = [mapping_configs] * len(num_units)
        mapping_base = mapping_dict[mapping_type]
        for num_unit, mapping_config in zip(num_units, mapping_configs):
            mappings.append(mapping_base(in_dim, num_unit, **mapping_config))
            in_dim = num_unit
        if out_dim is not None:
            if final_mapping_config is None:
                final_mapping_config = {}
            mappings.append(Linear(in_dim, out_dim, **final_mapping_config))
        self.mappings = ModuleList(mappings)

    @property
    def weights(self) -> List[Tensor]:
        return [mapping.weight for mapping in self.mappings]

    @property
    def biases(self) -> List[Optional[Tensor]]:
        return [mapping.bias for mapping in self.mappings]

    def forward(self, net: Tensor) -> Tensor:
        for mapping in self.mappings:
            net = mapping(net)
        return net

    @classmethod
    def simple(
        cls,
        in_dim: int,
        out_dim: Optional[int],
        num_units: List[int],
        *,
        bias: bool = False,
        dropout: float = 0.0,
        batch_norm: bool = False,
        activation: Optional[str] = None,
        pruner_config: Optional[Dict[str, Any]] = None,
    ) -> "MLP":
        mapping_config: Dict[str, Any]
        mapping_config = {
            "bias": bias,
            "dropout": dropout,
            "batch_norm": batch_norm,
            "pruner_config": pruner_config,
        }
        if activation is not None:
            mapping_config["activation"] = activation
        mapping_configs: Union[Dict[str, Any], List[Dict[str, Any]]]
        if activation != "glu":
            mapping_configs = mapping_config
        else:
            mapping_configs = []
            for num_unit in num_units:
                cfg = shallow_copy_dict(mapping_config)
                cfg["activation_config"] = {"in_dim": num_unit, "bias": bias}
                mapping_configs.append(cfg)
        final_mapping_config = {"bias": bias}
        return cls(
            in_dim,
            out_dim,
            num_units,
            mapping_configs,
            final_mapping_config=final_mapping_config,
        )

    @staticmethod
    def get_funnel_settings(
        max_dropout: float,
        max_dim: int,
        out_dim: int,
        num_layers: int,
    ) -> Tuple[List[float], List[int]]:
        dim = None
        dim_decrease = int(math.ceil((max_dim - out_dim) / num_layers))
        drop_decrease = max_dropout / num_layers
        dropouts = []
        num_units = []
        current_drop = max_dropout
        for i in range(num_layers):
            dropouts.append(current_drop)
            current_drop -= drop_decrease
            if i == 0:
                dim = max_dim
            else:
                assert dim is not None
                dim -= dim_decrease
            num_units.append(dim)
        return dropouts, num_units

    @classmethod
    def funnel(
        cls,
        in_dim: int,
        out_dim: int,
        max_dim: int,
        num_layers: int,
        *,
        bias: Optional[bool] = None,
        max_dropout: float = 0.1,
        batch_norm: bool = False,
        activation: Optional[str] = "relu",
        pruner_config: Optional[Dict[str, Any]] = None,
        final_mapping_config: Optional[Dict[str, Any]] = None,
    ) -> "MLP":
        dropouts, num_units = cls.get_funnel_settings(
            max_dropout,
            max_dim,
            out_dim,
            num_layers,
        )
        mapping_configs = []
        for dropout in dropouts:
            mapping_config: Dict[str, Any] = {
                "bias": bias,
                "dropout": dropout,
                "batch_norm": batch_norm,
                "pruner_config": pruner_config,
            }
            if activation is not None:
                mapping_config["activation"] = activation
            mapping_configs.append(mapping_config)
        return cls(
            in_dim,
            out_dim,
            num_units,
            mapping_configs,
            final_mapping_config=final_mapping_config,
        )


class LeafAggregation(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Any, *args: Any, **kwargs: Any) -> Tensor:
        net, leaves = args
        softmax_leaves = F.softmax(leaves, dim=1)
        ctx.save_for_backward(net, softmax_leaves.t())
        return net.mm(softmax_leaves)

    @staticmethod
    def backward(ctx: Any, *grad_outputs: Any) -> Tuple[Optional[Tensor], ...]:
        grad_output = grad_outputs[0]
        if grad_output is None:
            return None, None
        net, softmax_leaves = ctx.saved_tensors
        net_grad = grad_output.mm(softmax_leaves)
        sub_grad = grad_output.t().mm(net)
        sub_grad2 = (softmax_leaves * sub_grad).sum(0, keepdim=True)
        leaves_grad = softmax_leaves * (sub_grad - sub_grad2)
        return net_grad, leaves_grad.t()


class Route(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Any, *args: Any, **kwargs: Any) -> Tensor:
        (
            net,
            tree_arange,
            batch_indices,
            ones,
            increment_masks,
            num_tree,
            num_batch,
            tree_depth,
            num_internals,
        ) = args
        shape = num_batch, -1, num_internals
        sigmoid_net = torch.sigmoid(net)
        p_left = sigmoid_net.view(*shape).transpose(0, 1)
        p_right = 1.0 - p_left
        flat_probabilities = torch.cat([p_left, p_right], dim=-1)
        flat_probabilities = flat_probabilities.contiguous().view(num_tree, -1)
        current_indices = batch_indices + increment_masks[0]
        flat_dim = flat_probabilities.shape[-1]
        tree_arange = tree_arange * flat_dim
        routes = flat_probabilities.take(tree_arange + current_indices[None, ...])
        all_routes = [routes.clone()]
        for i in range(1, tree_depth + 1):
            current_indices = batch_indices + increment_masks[i]
            current_indices = tree_arange + current_indices[None, ...]
            current_routes = flat_probabilities.take(current_indices)
            all_routes.append(current_routes)
            routes *= current_routes
        ctx.save_for_backward(ones, sigmoid_net, *all_routes)
        ctx.tree_depth = tree_depth
        ctx.num_tree = num_tree
        return routes

    @staticmethod
    def backward(ctx: Any, *grad_outputs: Any) -> Tuple[Optional[Tensor], ...]:
        grad_output = grad_outputs[0]
        dummy_grads = tuple(None for _ in range(8))
        if grad_output is None:
            return (None,) + dummy_grads
        num_tree = ctx.num_tree
        tree_depth = ctx.tree_depth
        ones_list, sigmoid_net, *all_routes = ctx.saved_tensors
        cursor = 0
        divide = 1
        num_leaves = 2 ** (tree_depth + 1)
        sub_grads_shape = num_tree, sigmoid_net.shape[0], num_leaves - 1
        sub_grads = torch.zeros(*sub_grads_shape, device=grad_output.device)
        for i in range(tree_depth + 1):
            ones = ones_list[i]
            nodes = ones[None, None, ...]
            for j in range(tree_depth + 1):
                if j == i:
                    continue
                nodes = nodes * all_routes[j]
            sub_grad = grad_output * nodes
            section = int(round(num_leaves / divide))
            sub_grad = sub_grad.view(num_tree, -1, divide, section)
            sub_grad = sub_grad.sum(-1)
            sub_grads[..., cursor : cursor + divide] = sub_grad
            cursor += divide
            divide *= 2

        sub_grads = sub_grads.transpose(0, 1).contiguous()
        sub_grads = sub_grads.view(-1, num_tree * (num_leaves - 1))
        return (sigmoid_net * (1.0 - sigmoid_net) * sub_grads,) + dummy_grads


class DNDF(Module):
    def __init__(
        self,
        in_dim: int,
        out_dim: Optional[int],
        *,
        num_tree: int = 10,
        tree_depth: int = 4,
        is_regression: Optional[bool] = None,
        tree_proj_config: Optional[Dict[str, Any]] = None,
        use_fast_dndf: bool = True,
    ):
        super().__init__()
        self._num_tree = num_tree
        self._tree_depth = tree_depth
        self._is_regression = is_regression
        if out_dim is not None and is_regression is None:
            self._is_regression = out_dim == 1
        self._num_leaf = 2 ** (self._tree_depth + 1)
        self._num_internals = self._num_leaf - 1
        self._output_dim = out_dim
        self._fast = use_fast_dndf
        if tree_proj_config is None:
            tree_proj_config = {}
        tree_proj_config.setdefault("pruner_config", {})
        self.tree_proj = Linear(
            in_dim,
            self._num_internals * self._num_tree,
            **tree_proj_config,
        )
        if out_dim is None:
            self.leaves = None
        else:
            leaves_shape = self._num_tree * self._num_leaf, out_dim
            self.leaves = nn.Parameter(torch.empty(*leaves_shape))
            with torch.no_grad():
                torch.nn.init.xavier_uniform_(self.leaves.data)
        # buffers
        num_repeat, num_local_internals = self._num_leaf // 2, 1
        ones_np = np.repeat([1, -1], num_repeat)
        ones_list = [torch.from_numpy(ones_np.astype(np_float_type))]
        increment_indices_np = np.repeat([0, self._num_internals], num_repeat)
        increment_indices = [torch.from_numpy(increment_indices_np.astype(np_int_type))]
        for i in range(1, self._tree_depth + 1):
            num_repeat //= 2
            num_local_internals *= 2
            arange = np.arange(num_local_internals - 1, 2 * num_local_internals - 1)
            ones_np = np.repeat([1, -1], num_repeat)
            ones_np = np.tile(ones_np, 2 ** i)
            ones_list.append(torch.from_numpy(ones_np.astype(np_float_type)))
            increment_mask = np.repeat(arange, 2)
            increment_mask += np.tile([0, self._num_internals], num_local_internals)
            increment_mask = np.repeat(increment_mask, num_repeat)
            increment_mask_ = torch.from_numpy(increment_mask.astype(np_int_type))
            increment_indices.append(increment_mask_)
        self.increment_masks: Tensor
        self.register_buffer("tree_arange", torch.arange(num_tree)[..., None, None])
        self.register_buffer("ones", torch.stack(ones_list))
        self.register_buffer("increment_indices", torch.stack(increment_indices))

    def forward(self, net: Tensor) -> Tensor:
        num_batch = net.shape[0]
        tree_net = self.tree_proj(net)

        num_flat_prob = 2 * self._num_internals
        arange_args = 0, num_flat_prob * num_batch, num_flat_prob
        batch_indices = torch.arange(*arange_args, device=tree_net.device).view(-1, 1)

        if self._fast:
            routes = Route.apply(
                tree_net,
                self.tree_arange,
                batch_indices,
                self.ones,
                self.increment_indices,
                self._num_tree,
                num_batch,
                self._tree_depth,
                self._num_internals,
            )
        else:
            shape = num_batch, -1, self._num_internals
            p_left = torch.sigmoid(tree_net).view(*shape).transpose(0, 1)
            p_right = 1.0 - p_left
            flat_probabilities = torch.cat([p_left, p_right], dim=-1).contiguous()
            flat_probabilities = flat_probabilities.view(self._num_tree, -1)
            current_indices = batch_indices + self.increment_indices[0]  # type: ignore
            flat_dim = flat_probabilities.shape[-1]
            tree_arange = self.tree_arange * flat_dim  # type: ignore
            routes = flat_probabilities.take(tree_arange + current_indices[None, ...])
            for i in range(1, self._tree_depth + 1):
                current_indices = batch_indices + self.increment_indices[i]  # type: ignore
                current_indices = tree_arange + current_indices[None, ...]
                routes *= flat_probabilities.take(current_indices)

        features = routes.transpose(0, 1).contiguous().view(num_batch, -1)
        if self.leaves is None or self._output_dim is None:
            return features.view(num_batch, self._num_tree, -1)
        if self._is_regression or self._output_dim <= 1:
            outputs = features.mm(self.leaves)
        else:
            if self._fast:
                outputs = LeafAggregation.apply(features, self.leaves)
            else:
                leaves = F.softmax(self.leaves, dim=1)
                outputs = features.mm(leaves)
        return outputs / self._num_tree


class CrossBase(Module, metaclass=ABCMeta):
    @abstractmethod
    def forward(self, x: Tensor, x0: Tensor) -> Tensor:
        pass


class InnerCross(CrossBase):
    def __init__(self, dim: int, **kwargs: Any):
        super().__init__()
        self.inner = Linear(dim, 1, bias=False, **kwargs)

    def forward(self, x: Tensor, x0: Tensor) -> Tensor:
        return x0 * self.inner(x)


class CrossBlock(Module):
    def __init__(
        self,
        dim: int,
        bias: bool = True,
        residual: bool = True,
        *,
        cross_builder: Callable[[int], Module] = None,
        **kwargs: Any,
    ):
        super().__init__()
        if cross_builder is None:
            cross_builder = lambda dim_: InnerCross(dim_)
        self.cross = cross_builder(dim)
        if not bias:
            self.bias = None
        else:
            self.bias = nn.Parameter(torch.empty(1, dim))
            with torch.no_grad():
                self.bias.data.fill_(kwargs.get("bias_fill", 0.0))
        self.residual = residual

    def forward(self, x: Tensor, x0: Tensor) -> Tensor:
        crossed = self.cross(x, x0)
        if self.residual:
            crossed = crossed + x
        if self.bias is None:
            return crossed
        return crossed + self.bias

    def extra_repr(self) -> str:
        return f"(bias): {False if self.bias is None else True}"


class TreeResBlock(Module):
    def __init__(self, dim: int, dndf_config: Optional[Dict[str, Any]] = None):
        super().__init__()
        if dndf_config is None:
            dndf_config = {}
        self.dim = float(dim)
        self.in_dndf = DNDF(dim, dim, **shallow_copy_dict(dndf_config))
        self.inner_dndf = DNDF(dim, dim, **shallow_copy_dict(dndf_config))

    def forward(self, net: Tensor) -> Tensor:
        res = self.in_dndf(net)
        res = self.dim * res - 1.0
        res = self.inner_dndf(res)
        res = self.dim * res - 1.0
        return net + res


class InvertibleBlock(Module):
    def __init__(
        self,
        dim: int,
        *,
        default_activation: str = "mish",
        transition_builder: Callable[[int], Module] = None,
    ):
        if dim % 2 != 0:
            raise ValueError("`dim` should be divided by 2")
        super().__init__()
        h_dim = int(dim // 2)
        # transition
        if transition_builder is not None:
            transition = transition_builder(dim)
        else:
            transition = MLP.simple(
                h_dim,
                None,
                [h_dim],
                activation=default_activation,
            )
        self.transition = transition

    def forward(self, net1: Tensor, net2: Tensor) -> tensor_tuple_type:
        net1 = net1 + self.transition(net2)
        return net2, net1

    def inverse(self, net1: Tensor, net2: Tensor) -> tensor_tuple_type:
        net2 = net2 - self.transition(net1)
        return net2, net1


class ConditionalOutput(NamedTuple):
    net: Tensor
    cond: Tensor
    responses: List[Tensor]


class PseudoInvertibleBlock(Module):
    def __init__(
        self,
        in_dim: int,
        latent_dim: int,
        out_dim: int,
        *,
        to_activation: str = "mish",
        from_activation: str = "mish",
        to_transition_builder: Optional[Callable[[int, int], Module]] = None,
        from_transition_builder: Optional[Callable[[int, int], Module]] = None,
    ):
        super().__init__()
        if to_transition_builder is not None:
            self.to_latent = to_transition_builder(in_dim, latent_dim)
        else:
            num_units = [latent_dim, latent_dim, latent_dim]
            self.to_latent = MLP.simple(
                in_dim,
                None,
                num_units,
                activation=to_activation,
            )
        if from_transition_builder is not None:
            self.from_latent = from_transition_builder(latent_dim, out_dim)
        else:
            self.from_latent = MLP.simple(
                latent_dim,
                out_dim,
                [latent_dim, latent_dim],
                bias=True,
                activation=from_activation,
            )

    def forward(
        self,
        net: Union[Tensor, Any],
        cond: Optional[Union[Tensor, Any]] = None,
    ) -> Union[Tensor, Any]:
        if cond is None:
            return self.to_latent(net)
        return self.to_latent(net, cond)

    def inverse(
        self,
        net: Union[Tensor, Any],
        cond: Optional[Union[Tensor, Any]] = None,
    ) -> Union[Tensor, Any]:
        if cond is None:
            return self.from_latent(net)
        return self.from_latent(net, cond)


class MonotonousMapping(Module):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        *,
        ascent: bool,
        bias: bool = True,
        dropout: float = 0.0,
        batch_norm: bool = False,
        activation: Optional[str] = None,
        init_method: Optional[str] = "xavier_uniform",
        positive_transform: str = "square",
        scaler: Optional[float] = None,
        use_scaler: bool = True,
        **kwargs: Any,
    ):
        super().__init__()
        self.ascent = ascent
        self.positive_transform = positive_transform
        self.config = shallow_copy_dict(kwargs)
        # linear
        self.linear = Linear(
            in_dim,
            out_dim,
            bias=bias,
            init_method=init_method,
            **kwargs,
        )
        # dropout
        use_dropout = 0.0 < dropout < 1.0
        self.dropout = None if not use_dropout else Dropout(dropout)
        # batch norm
        self.bn = None if not batch_norm else BN(out_dim)
        # activation
        if activation is None:
            self.activation: Optional[Module] = None
        else:
            activation_config = self.config.setdefault("activation_config", None)
            self.activation = Activations.make(activation, activation_config)
        # scaler
        if not use_scaler:
            self.scaler = None
        else:
            if scaler is None:
                scaler = math.log(math.e - 1)
            self.scaler = nn.Parameter(torch.full([out_dim, 1], scaler))

    def _get_positive_weight(self) -> Tensor:
        weight = self.linear.weight
        if self.positive_transform == "abs":
            pos_weight = torch.abs(weight)
        elif self.positive_transform == "square":
            pos_weight = weight ** 2
        elif self.positive_transform == "sigmoid":
            pos_weight = torch.sigmoid(weight)
        elif self.positive_transform == "softmax":
            pos_weight = F.softmax(weight, dim=1)
        elif self.positive_transform == "softplus":
            pos_weight = F.softplus(weight)
        else:
            msg = f"positive transform '{self.positive_transform}' is not implemented"
            raise NotImplementedError(msg)
        if self.scaler is None:
            return pos_weight
        scaler = F.softplus(self.scaler)
        return scaler * pos_weight

    def forward(self, net: Tensor, *, reuse: bool = False) -> Tensor:
        weight = self._get_positive_weight()
        if not self.ascent:
            weight = -weight
        net = F.linear(net, weight, self.linear.bias)
        if self.bn is not None:
            net = self.bn(net)
        if self.activation is not None:
            net = self.activation(net)
        if self.dropout is not None:
            net = self.dropout(net, reuse=reuse)
        return net

    def extra_repr(self) -> str:
        msg = f"(ascent): {self.ascent}\n(positive): {self.positive_transform}"
        if self.scaler is None:
            return msg
        return f"{msg}\n(scaler): {self.scaler.shape}"

    @classmethod
    def make_couple(
        cls,
        in_dim: int,
        hidden_dim: int,
        out_dim: int,
        activation: str,
        *,
        ascent: bool,
        bias: bool = True,
        dropout: float = 0.0,
        batch_norm: bool = False,
        use_residual: bool = False,
        use_inverse_activation: bool = True,
        scaler: Optional[float] = None,
        init_method: Optional[str] = "normal",
        **kwargs: Any,
    ) -> Module:
        if not use_inverse_activation:
            inverse_activation = None
        elif activation == "tanh":
            inverse_activation = "atanh"
        elif activation == "sigmoid":
            inverse_activation = "logit"
        elif activation == "softplus":
            inverse_activation = "isoftplus"
        else:
            msg = f"inverse activation of '{activation}' is not defined"
            raise NotImplementedError(msg)
        initialize_config = kwargs.setdefault("initialize_config", {})
        initialize_config.setdefault("std", 3.0)
        squash_unit = cls(
            in_dim,
            hidden_dim,
            ascent=ascent,
            bias=bias,
            dropout=dropout,
            batch_norm=batch_norm,
            activation=activation,
            init_method=init_method,
            positive_transform="softmax" if in_dim > 1 else "softplus",
            scaler=scaler,
            **kwargs,
        )
        inverse_unit = cls(
            hidden_dim,
            out_dim,
            ascent=True,
            bias=False,
            dropout=dropout,
            batch_norm=batch_norm,
            activation=inverse_activation,
            init_method=init_method,
            positive_transform="softmax",
            use_scaler=False,
            **kwargs,
        )

        class Couple(Module):
            def __init__(self) -> None:
                super().__init__()
                self.squash = squash_unit
                self.inverse = inverse_unit
                self.use_residual = use_residual

            def forward(self, net: Tensor) -> Tensor:
                squashed = self.squash(net)
                inversed = self.inverse(squashed)
                if not self.use_residual:
                    return inversed
                if in_dim == out_dim:
                    return net + inversed
                if hidden_dim == out_dim:
                    return squashed + inversed
                raise ValueError(
                    "either `in_dim` or `hidden_dim` should be identical with "
                    "`out_dim` when `use_residual` is True"
                )

            def extra_repr(self) -> str:
                return f"(residual): {self.use_residual}"

        return Couple()

    @classmethod
    def stack(
        cls,
        in_dim: int,
        out_dim: Optional[int],
        num_units: List[int],
        *,
        ascent: bool,
        bias: bool = False,
        dropout: float = 0.0,
        batch_norm: bool = False,
        final_batch_norm: bool = False,
        use_couple: bool = True,
        use_couple_bias: bool = True,
        use_couple_residual: bool = False,
        use_couple_inverse_activation: bool = True,
        activation: Optional[str] = "sigmoid",
        init_method: Optional[str] = "normal",
        positive_transform: str = "softmax",
        use_scaler: bool = True,
        scaler: Optional[float] = None,
        return_blocks: bool = False,
        **kwargs: Any,
    ) -> Union[List[Module], Module]:
        blocks = []
        common_kwargs = {
            "ascent": ascent,
            "dropout": dropout,
            "batch_norm": batch_norm,
            "activation": activation,
        }

        def _make(
            in_dim_: int,
            out_dim_: int,
            hidden_dim: int,
            use_residual: bool,
            use_inverse_activation: bool,
        ) -> Module:
            local_kwargs = shallow_copy_dict(common_kwargs)
            local_kwargs.update(shallow_copy_dict(kwargs))
            local_kwargs["in_dim"] = in_dim_
            local_kwargs["out_dim"] = out_dim_
            if use_couple:
                local_kwargs["scaler"] = scaler
                local_kwargs["hidden_dim"] = hidden_dim
                local_kwargs["use_residual"] = use_residual
                local_kwargs["use_inverse_activation"] = use_inverse_activation
                local_kwargs["bias"] = use_couple_bias
                return cls.make_couple(**local_kwargs)
            local_kwargs["bias"] = bias
            local_kwargs["init_method"] = init_method
            local_kwargs["positive_transform"] = positive_transform
            local_kwargs["use_scaler"] = use_scaler
            return cls(**local_kwargs)

        current_in_dim = in_dim
        for num_unit in num_units:
            blocks.append(
                _make(
                    current_in_dim,
                    num_unit,
                    num_unit,
                    use_couple_residual,
                    True,
                )
            )
            common_kwargs["ascent"] = True
            current_in_dim = num_unit
        if out_dim is not None:
            common_kwargs["batch_norm"] = final_batch_norm
            blocks.append(
                _make(
                    current_in_dim,
                    out_dim,
                    current_in_dim,
                    False,
                    use_couple_inverse_activation,
                )
            )

        if return_blocks:
            return blocks
        return nn.Sequential(*blocks)


class ConditionalBlocks(Module):
    def __init__(
        self,
        main_blocks: ModuleList,
        condition_blocks: ModuleList,
        detach_condition: bool = False,
        *,
        add_last: bool,
        cond_mixtures: Optional[ModuleList] = None,
    ):
        super().__init__()
        self.add_last = add_last
        self.detach_condition = detach_condition
        self.num_blocks = len(main_blocks)
        if self.num_blocks != len(condition_blocks):
            msg = "`main_blocks` and `condition_blocks` should have same sizes"
            raise ValueError(msg)
        self.main_blocks = main_blocks
        self.condition_blocks = condition_blocks
        self.cond_mixtures = cond_mixtures

    def forward(
        self,
        net: Tensor,
        cond: Union[Tensor, List[Tensor]],
    ) -> ConditionalOutput:
        if isinstance(cond, list):
            cond_responses = cond
            detached_responses = [net.detach() for net in cond]
        else:
            cond_responses = []
            detached_responses = []
            for condition in self.condition_blocks:
                cond = condition(cond)
                cond_responses.append(cond)  # type: ignore
                detached_responses.append(cond.detach())  # type: ignore
        responses = detached_responses if self.detach_condition else cond_responses
        iterator = enumerate(zip(self.main_blocks, responses))
        for i, (main, response) in iterator:
            net = main(net)
            if i < self.num_blocks - 1 or self.add_last:
                if self.cond_mixtures is None:
                    net = net + response
                else:
                    net = self.cond_mixtures[i](net, response)
        return ConditionalOutput(net, cond_responses[-1], responses)

    def extra_repr(self) -> str:
        add_last = f"(add_last): {self.add_last}"
        detach_condition = f"(detach_condition): {self.detach_condition}"
        return f"{add_last}\n{detach_condition}"


class AttentionOutput(NamedTuple):
    output: Tensor
    weights: Tensor


attentions: Dict[str, Type["Attention"]] = {}


class Attention(Module):
    def __init__(
        self,
        input_dim: int,
        num_heads: int = 1,
        *,
        dropout: float = 0.0,
        is_self_attention: bool = False,
        k_dim: Optional[int] = None,
        v_dim: Optional[int] = None,
        embed_dim: Optional[int] = None,
        activation: Optional[str] = None,
        activation_config: Optional[Dict[str, Any]] = None,
        q_linear_config: Optional[Dict[str, Any]] = None,
        k_linear_config: Optional[Dict[str, Any]] = None,
        v_linear_config: Optional[Dict[str, Any]] = None,
        in_linear_config: Optional[Dict[str, Any]] = None,
        out_linear_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.is_self_attn = is_self_attention
        if not is_self_attention:
            self.k_dim = k_dim if k_dim is not None else input_dim
            self.v_dim = v_dim if v_dim is not None else input_dim
        else:
            if k_dim is not None and k_dim != input_dim:
                raise ValueError("self attention is used but `k_dim` != `input_dim`")
            if v_dim is not None and v_dim != input_dim:
                raise ValueError("self attention is used but `v_dim` != `input_dim`")
            self.k_dim = self.v_dim = input_dim
        if embed_dim is None:
            embed_dim = min(32, input_dim) * num_heads
        self.embed_dim = embed_dim

        self.num_heads = num_heads
        self.head_dim = self.embed_dim // num_heads
        self.scaling = float(self.head_dim) ** -0.5
        if self.head_dim * num_heads != self.embed_dim:
            raise ValueError("`embed_dim` must be divisible by `num_heads`")

        def _warn(prefix: str) -> None:
            msg = (
                f"self attention is used so `{prefix}_linear_config` will be ignored, "
                "please use `in_linear_config` instead"
            )
            print(f"{LoggingMixin.warning_prefix}{msg}")

        if q_linear_config is None:
            q_linear_config = {}
        elif is_self_attention:
            _warn("q")
        if k_linear_config is None:
            k_linear_config = {}
        elif is_self_attention:
            _warn("k")
        if v_linear_config is None:
            v_linear_config = {}
        elif is_self_attention:
            _warn("v")

        if is_self_attention:
            if in_linear_config is None:
                in_linear_config = {}
            self.in_linear = Linear(input_dim, 3 * self.embed_dim, **in_linear_config)
        else:
            self.q_linear = Linear(input_dim, self.embed_dim, **q_linear_config)
            self.k_linear = Linear(self.k_dim, self.embed_dim, **k_linear_config)
            self.v_linear = Linear(self.v_dim, self.embed_dim, **v_linear_config)

        if out_linear_config is None:
            out_linear_config = {}
        self.out_linear = Linear(self.embed_dim, input_dim, **out_linear_config)

        self.dropout = dropout
        self.activation = Activations.make(activation, activation_config)

    def _to_heads(self, tensor: Tensor) -> Tensor:
        batch_size, seq_len, in_feature = tensor.shape
        tensor = tensor.view(batch_size, seq_len, self.num_heads, self.head_dim)
        return tensor.permute(0, 2, 1, 3).contiguous().view(-1, seq_len, self.head_dim)

    def _get_weights(self, raw_weights: Tensor) -> Tensor:
        # in most cases the softmax version is good enough
        return F.softmax(raw_weights, dim=-1)

    def _weights_callback(self, weights: Tensor) -> Tensor:
        return weights

    def forward(
        self,
        q: Tensor,
        k: Tensor,
        v: Tensor,
        *,
        mask: Optional[Tensor] = None,
    ) -> AttentionOutput:
        # `mask` represents slots which will be zeroed
        k_len = k.shape[1]
        if self.is_self_attn:
            q, k, v = self.in_linear(q).chunk(3, dim=-1)
        else:
            # B, Sq, Din -> B, Sq, D
            q = self.q_linear(q)
            # B, Sk, Dk -> B, Sk, D
            k = self.k_linear(k)
            # B, Sv, Dv -> B, Sk, D
            v = self.v_linear(v)
        q, k, v = map(self.activation, [q, k, v])
        # scale
        q = q * self.scaling
        # B, S*, D -> B * N_head, S*, D_head
        q, k, v = map(self._to_heads, [q, k, v])
        if mask is not None:
            # B, Sq, Sk -> B * N_head, Sq, Sk
            mask = mask.repeat(self.num_heads, 1, 1)
        # B * N_head, Sq, Sk
        raw_weights = torch.bmm(q, k.transpose(-2, -1))
        if mask is not None:
            raw_weights.masked_fill_(mask, float("-inf"))
        # B * N_head, Sq, Sk -> # B * N_head, Sq, Sk
        weights = self._get_weights(raw_weights)
        if 0.0 < self.dropout < 1.0:
            weights = F.dropout(weights, self.dropout, self.training)
        weights = self._weights_callback(weights)
        # B * N_head, Sq, D_head
        output = torch.bmm(weights, v)
        # B * N_head, Sq, D_head -> B, N_head, Sq, D_head
        nb, q_len, d_head = output.shape
        output = output.view(nb // self.num_heads, self.num_heads, q_len, d_head)
        # B, N_head, Sq, D_head -> B, Sq, D
        output = output.permute(0, 2, 1, 3).contiguous()
        output = output.view(-1, q_len, self.embed_dim)
        # B, Sq, D -> B, Sq, Din
        output = self.activation(self.out_linear(output))
        return AttentionOutput(output, weights.view(-1, self.num_heads, q_len, k_len))

    @classmethod
    def get(cls, name: str) -> Type["Attention"]:
        return attentions[name]

    @classmethod
    def register(cls, name: str) -> Callable[[Type], Type]:
        global attentions
        return register_core(name, attentions)


Attention.register("basic")(Attention)


__all__ = [
    "Linear",
    "Mapping",
    "MLP",
    "DNDF",
    "CrossBlock",
    "TreeResBlock",
    "InvertibleBlock",
    "PseudoInvertibleBlock",
    "MonotonousMapping",
    "ConditionalBlocks",
    "ConditionalOutput",
    "Attention",
]
