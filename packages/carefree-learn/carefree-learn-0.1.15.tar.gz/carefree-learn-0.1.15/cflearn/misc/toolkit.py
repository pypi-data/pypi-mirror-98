import os
import math
import torch
import inspect
import logging
import platform

import numpy as np
import torch.nn as nn

from typing import *
from abc import abstractmethod
from abc import ABCMeta
from argparse import Namespace
from functools import partial
from collections import defaultdict
from collections import OrderedDict
from cftool.misc import prod
from cftool.misc import shallow_copy_dict
from cftool.misc import context_error_handler
from cftool.misc import LoggingMixin
from cfdata.types import np_int_type
from cfdata.types import np_float_type

from ..types import data_type
from ..types import param_type
from ..types import np_dict_type
from ..types import tensor_dict_type


def is_int(arr: np.ndarray) -> bool:
    return np.issubdtype(arr.dtype, np.integer)


def is_float(arr: np.ndarray) -> bool:
    return np.issubdtype(arr.dtype, np.floating)


def to_standard(arr: np.ndarray) -> np.ndarray:
    if is_int(arr):
        arr = arr.astype(np_int_type)
    elif is_float(arr):
        arr = arr.astype(np_float_type)
    return arr


def to_torch(arr: np.ndarray) -> torch.Tensor:
    return torch.from_numpy(to_standard(arr))


def to_numpy(tensor: torch.Tensor) -> np.ndarray:
    return tensor.detach().cpu().numpy()


def to_2d(arr: data_type) -> data_type:
    if arr is None or isinstance(arr, str):
        return None
    if isinstance(arr, np.ndarray):
        return arr.reshape([len(arr), -1])
    if isinstance(arr[0], list):
        return arr
    return [[elem] for elem in arr]  # type: ignore


def to_prob(raw: np.ndarray) -> np.ndarray:
    return nn.functional.softmax(torch.from_numpy(raw), dim=1).numpy()


def collate_np_dicts(ds: List[np_dict_type], axis: int = 0) -> np_dict_type:
    results = {}
    d0 = ds[0]
    for k in d0.keys():
        if not isinstance(d0[k], np.ndarray):
            continue
        arrays = []
        for rs in ds:
            array = rs[k]
            if len(array.shape) == 0:
                array = array.reshape([1])
            arrays.append(array)
        results[k] = np.concatenate(arrays, axis=axis)
    return results


def collate_tensor_dicts(ds: List[tensor_dict_type], dim: int = 0) -> tensor_dict_type:
    results = {}
    d0 = ds[0]
    for k in d0.keys():
        if not isinstance(d0[k], torch.Tensor):
            continue
        tensors = []
        for rs in ds:
            tensor = rs[k]
            if len(tensor.shape) == 0:
                tensor = tensor.view([1])
            tensors.append(tensor)
        results[k] = torch.cat(tensors, dim=dim)
    return results


def switch_requires_grad(params: List[nn.Parameter], requires_grad: bool) -> None:
    for param in params:
        param.requires_grad_(requires_grad)


def get_gradient(
    y: torch.Tensor,
    x: torch.Tensor,
    retain_graph: bool = False,
    create_graph: bool = False,
) -> Union[torch.Tensor, Tuple[torch.Tensor, ...]]:
    grads = torch.autograd.grad(y, x, torch.ones_like(y), retain_graph, create_graph)
    if len(grads) == 1:
        return grads[0]
    return grads


def scheduler_requires_metric(scheduler: Any) -> bool:
    signature = inspect.signature(scheduler.step)
    for name, param in signature.parameters.items():
        if param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if name == "metrics":
                return True
    return False


def parse_uri(path: str) -> str:
    delim = "/" if platform.system() == "Windows" else ""
    return f"file://{delim}{path}"


def to_relative(abs_folder: str, root_abs_folder: str) -> str:
    common_prefix = os.path.commonpath([root_abs_folder, abs_folder])
    return os.path.relpath(abs_folder, common_prefix)


def parse_args(args: Any) -> Namespace:
    return Namespace(**{k: None if not v else v for k, v in args.__dict__.items()})


def parse_path(path: Optional[str], root_dir: Optional[str]) -> Optional[str]:
    if path is None:
        return None
    if root_dir is None:
        return path
    return os.path.abspath(os.path.join(root_dir, path))


def inject_mlflow_stuffs(
    model: str,
    *,
    config: Dict[str, Any],
    run_name: Optional[str] = None,
    run_name_prefix: Optional[str] = None,
) -> None:
    unwanted_keys = [
        "cuda",
        "use_tqdm",
        "mlflow_config",
        "verbose_level",
        "trigger_logging",
    ]
    mlflow_config = config.get("mlflow_config")
    if mlflow_config is not None:
        # run name
        if run_name is not None:
            mlflow_config["run_name"] = run_name
        if run_name_prefix is not None:
            mlflow_config["run_name_prefix"] = run_name_prefix
        # mlflow params
        if "mlflow_params" not in mlflow_config:
            mlflow_params = {}

            def flatten(d: Dict[str, Any], previous_keys: Tuple[str, ...]) -> None:
                for k, v in d.items():
                    if isinstance(v, dict):
                        flatten(v, previous_keys + (k,))
                        continue
                    cursor = -1
                    while k in mlflow_params:
                        if cursor < -len(previous_keys):
                            raise ValueError("internal error occurred")
                        k = f"{previous_keys[cursor]}_{k}"
                        cursor -= 1
                    mlflow_params[k] = v

            for_flatten = shallow_copy_dict(config)
            for key in unwanted_keys:
                for_flatten.pop(key, None)
            flatten(for_flatten, ())
            mlflow_params["model"] = model
            mlflow_config["mlflow_params"] = mlflow_params


# This is a modified version of https://github.com/sksq96/pytorch-summary
#  So it can summary `carefree-learn` model structures better
def summary(model: nn.Module, sample_batch: tensor_dict_type) -> None:
    def register_hook(module: nn.Module) -> None:
        def hook(module_: nn.Module, inp: Any, output: Any) -> None:
            m_name = module_names.get(module_)
            if m_name is None:
                return

            inp = inp[0]
            if not isinstance(inp, torch.Tensor):
                return
            if isinstance(output, (list, tuple)):
                for element in output:
                    if not isinstance(element, torch.Tensor):
                        return
            elif not isinstance(output, torch.Tensor):
                return

            m_dict: OrderedDict[str, Any] = OrderedDict()
            m_dict["input_shape"] = list(inp.size())
            m_dict["input_shape"][0] = -1
            if isinstance(output, (list, tuple)):
                m_dict["output_shape"] = [[-1] + list(o.size())[1:] for o in output]
                m_dict["is_multiple_output"] = True
            else:
                m_dict["output_shape"] = list(output.size())
                m_dict["output_shape"][0] = -1
                m_dict["is_multiple_output"] = False

            num_params_ = 0
            num_trainable_params_ = 0
            for param in module_.parameters():
                local_num_params = int(round(prod(param.data.shape)))
                num_params_ += local_num_params
                if param.requires_grad:
                    num_trainable_params_ += local_num_params
            m_dict["num_params"] = num_params_
            m_dict["num_trainable_params"] = num_trainable_params_
            raw_summary_dict[m_name] = m_dict

        if not isinstance(module, torch.jit.ScriptModule):
            hooks.append(module.register_forward_hook(hook))

    # get names
    def _inject_names(m: nn.Module, previous_names: List[str]) -> None:
        info_list = []
        for child in m.children():
            current_names = previous_names + [type(child).__name__]
            current_name = ".".join(current_names)
            module_names[child] = current_name
            info_list.append((child, current_name, current_names))
        counts: Dict[str, int] = defaultdict(int)
        idx_mapping: Dict[nn.Module, int] = {}
        for child, current_name, _ in info_list:
            idx_mapping[child] = counts[current_name]
            counts[current_name] += 1
        for child, current_name, current_names in info_list:
            if counts[current_name] == 1:
                continue
            current_name = f"{current_name}-{idx_mapping[child]}"
            module_names[child] = current_name
            current_names[-1] = current_name.split(".")[-1]
        for child, _, current_names in info_list:
            _inject_names(child, current_names)

    module_names: OrderedDict[nn.Module, str] = OrderedDict()
    existing_names: Set[str] = set()

    def _get_name(original: str) -> str:
        count = 0
        final_name = original
        while final_name in existing_names:
            count += 1
            final_name = f"{original}_{count}"
        existing_names.add(final_name)
        return final_name

    for extractor in model.extractors.values():  # type: ignore
        extractor_name = _get_name(type(extractor).__name__)
        module_names[extractor] = extractor_name
        _inject_names(extractor, [extractor_name])
    for head in model.heads.values():  # type: ignore
        head_name = _get_name(type(head).__name__)
        module_names[head] = head_name
        _inject_names(head, [head_name])

    # create properties
    raw_summary_dict: OrderedDict[str, Any] = OrderedDict()
    hooks: List[Any] = []

    # register hook
    model.apply(register_hook)

    # make a forward pass
    model(sample_batch)

    # remove these hooks
    for h in hooks:
        h.remove()

    # get hierarchy
    hierarchy: OrderedDict[str, Any] = OrderedDict()
    for key in raw_summary_dict:
        split = key.split(".")
        d = hierarchy
        for elem in split[:-1]:
            d = d.setdefault(elem, OrderedDict())
        d.setdefault(split[-1], None)

    # reconstruct summary_dict
    def _inject_summary(current_hierarchy: Any, previous_keys: List[str]) -> None:
        if previous_keys and not previous_keys[-1]:
            previous_keys.pop()
        current_layer = len(previous_keys)
        current_count = hierarchy_counts.get(current_layer, 0)
        prefix = "  " * current_layer
        nonlocal total_params  # type: ignore
        nonlocal trainable_params  # type: ignore
        for k, v in current_hierarchy.items():
            current_keys = previous_keys + [k]
            concat_k = ".".join(current_keys)
            current_summary = raw_summary_dict.get(concat_k)
            if current_summary is not None:
                summary_dict[f"{prefix}{k}-{current_count}"] = current_summary
                hierarchy_counts[current_layer] = current_count + 1
                if current_layer == 0:
                    total_params += current_summary["num_params"]
                    trainable_params += current_summary["num_trainable_params"]
            if v is not None:
                _inject_summary(v, current_keys)

    total_params = 0
    trainable_params = 0
    hierarchy_counts: Dict[int, int] = {}
    summary_dict: OrderedDict[str, Any] = OrderedDict()
    _inject_summary(hierarchy, [])

    line_length = 120
    print("=" * line_length)
    line_format = "{:30}  {:>20} {:>40} {:>20}"
    headers = "Layer (type)", "Input Shape", "Output Shape", "Trainable Param #"
    line_new = line_format.format(*headers)
    print(line_new)
    print("-" * line_length)
    total_output = 0
    for layer in summary_dict:
        # name, input_shape, output_shape, num_trainable_params
        line_new = line_format.format(
            "-".join(layer.split("-")[:-1]),
            str(summary_dict[layer]["input_shape"]),
            str(summary_dict[layer]["output_shape"]),
            "{0:,}".format(summary_dict[layer]["num_trainable_params"]),
        )
        output_shape = summary_dict[layer]["output_shape"]
        is_multiple_output = summary_dict[layer]["is_multiple_output"]
        if not is_multiple_output:
            output_shape = [output_shape]
        for shape in output_shape:
            total_output += prod(shape)
        print(line_new)

    # assume 4 bytes/number (float on cuda).
    x_batch = sample_batch["x_batch"]
    total_input_size = abs(prod(x_batch.shape[1:]) * 4.0 / (1024 ** 2.0))
    # x2 for gradients
    total_output_size = abs(2.0 * total_output * 4.0 / (1024 ** 2.0))
    total_params_size = abs(total_params * 4.0 / (1024 ** 2.0))
    total_size = total_params_size + total_output_size + total_input_size

    print("=" * line_length)
    print("Total params: {0:,}".format(total_params))
    print("Trainable params: {0:,}".format(trainable_params))
    print("Non-trainable params: {0:,}".format(total_params - trainable_params))
    print("-" * line_length)
    print("Input size (MB): %0.2f" % total_input_size)
    print("Forward/backward pass size (MB): %0.2f" % total_output_size)
    print("Params size (MB): %0.2f" % total_params_size)
    print("Estimated Total Size (MB): %0.2f" % total_size)
    print("-" * line_length)


class LoggingMixinWithRank(LoggingMixin):
    is_rank_0: bool = True

    def set_rank_0(self, value: bool) -> None:
        self.is_rank_0 = value
        for v in self.__dict__.values():
            if isinstance(v, LoggingMixinWithRank):
                v.set_rank_0(value)

    def _init_logging(
        self,
        verbose_level: Optional[int] = 2,
        trigger: bool = True,
    ) -> None:
        if not self.is_rank_0:
            return None
        super()._init_logging(verbose_level, trigger)

    def log_msg(
        self,
        body: str,
        prefix: str = "",
        verbose_level: Optional[int] = 1,
        msg_level: int = logging.INFO,
        frame: Any = None,
    ) -> None:
        if not self.is_rank_0:
            return None
        super().log_msg(body, prefix, verbose_level, msg_level, frame)

    def log_block_msg(
        self,
        body: str,
        prefix: str = "",
        title: str = "",
        verbose_level: Optional[int] = 1,
        msg_level: int = logging.INFO,
        frame: Any = None,
    ) -> None:
        if not self.is_rank_0:
            return None
        super().log_block_msg(body, prefix, title, verbose_level, msg_level, frame)

    def log_timing(self) -> None:
        if not self.is_rank_0:
            return None
        return super().log_timing()


class Initializer(LoggingMixinWithRank):
    """
    Initializer for neural network weights

    Examples
    --------
    >>> initializer = Initializer()
    >>> linear = nn.Linear(10, 10)
    >>> initializer.xavier_uniform(linear.weight)

    """

    defined_initialization = {
        "xavier_uniform",
        "xavier_normal",
        "normal",
        "truncated_normal",
    }
    custom_initializer: Dict[str, Callable] = {}

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._verbose_level = self.config.setdefault("verbose_level", 2)

    def initialize(self, param: param_type, method: str) -> Any:
        custom_initializer = self.custom_initializer.get(method)
        if custom_initializer is None:
            return getattr(self, method)(param)
        return custom_initializer(self, param)

    @classmethod
    def add_initializer(cls, f: Callable, name: str) -> None:
        if name in cls.defined_initialization:
            print(f"{cls.warning_prefix}'{name}' initializer is already defined")
            return
        cls.defined_initialization.add(name)
        cls.custom_initializer[name] = f

    def xavier_uniform(self, param: param_type) -> None:
        gain = self.config.setdefault("gain", 1.0)
        nn.init.xavier_uniform_(param.data, gain)

    def xavier_normal(self, param: param_type) -> None:
        gain = self.config.setdefault("gain", 1.0)
        nn.init.xavier_normal_(param.data, gain)

    def normal(self, param: param_type) -> None:
        mean = self.config.setdefault("mean", 0.0)
        std = self.config.setdefault("std", 1.0)
        with torch.no_grad():
            param.data.normal_(mean, std)

    def truncated_normal(self, param: param_type) -> None:
        span = self.config.setdefault("span", 2.0)
        mean = self.config.setdefault("mean", 0.0)
        std = self.config.setdefault("std", 1.0)
        tol = self.config.setdefault("tol", 0.0)
        epoch = self.config.setdefault("epoch", 20)
        num_elem = param.numel()
        weight_base = param.new_empty(num_elem).normal_()
        get_invalid = lambda w: (w > span) | (w < -span)
        invalid = get_invalid(weight_base)
        success = False
        for _ in range(epoch):
            num_invalid = invalid.sum().item()
            if num_invalid / num_elem <= tol:
                success = True
                break
            with torch.no_grad():
                weight_base[invalid] = param.new_empty(num_invalid).normal_()
                invalid = get_invalid(weight_base)
        if not success:
            self.log_msg(
                f"invalid ratio for truncated normal : {invalid.to(torch.float32).mean():8.6f}, "
                f"it might cause by too little epoch ({epoch}) or too small tolerance ({tol})",
                prefix=self.warning_prefix,
                verbose_level=2,
                msg_level=logging.WARNING,
            )
        with torch.no_grad():
            param.data.copy_(weight_base.reshape(param.shape))
            param.data.mul_(std).add_(mean)

    def orthogonal(self, param: param_type) -> None:
        gain = self.config.setdefault("gain", 1.0)
        nn.init.orthogonal_(param.data, gain)


class _multiplied_activation(nn.Module, metaclass=ABCMeta):
    def __init__(
        self,
        ratio: float,
        trainable: bool = True,
    ):
        super().__init__()
        self.trainable = trainable
        ratio_ = torch.tensor([ratio], dtype=torch.float32)
        self.ratio = ratio_ if not trainable else nn.Parameter(ratio_)

    @abstractmethod
    def _core(self, multiplied: torch.Tensor) -> torch.Tensor:
        pass

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self._core(x * self.ratio)

    def extra_repr(self) -> str:
        return f"ratio={self.ratio.item()}, trainable={self.trainable}"


class Lambda(nn.Module):
    def __init__(self, fn: Callable, name: str = None):
        super().__init__()
        self.name = name
        self.fn = fn

    def extra_repr(self) -> str:
        return "" if self.name is None else self.name

    def forward(self, *args: Any, **kwargs: Any) -> Any:
        return self.fn(*args, **kwargs)


class Activations:
    """
    Wrapper class for pytorch activations
    * when pytorch implemented corresponding activation, it will be returned
    * otherwise, custom implementation will be returned

    Parameters
    ----------
    configs : {None, dict}, configuration for the activation

    Examples
    --------
    >>> act = Activations()
    >>> print(type(act.ReLU))  # <class 'nn.modules.activation.ReLU'>
    >>> print(type(act.module("ReLU")))  # <class 'nn.modules.activation.ReLU'>
    >>> print(type(act.Tanh))  # <class 'nn.modules.activation.Tanh'>
    >>> print(type(act.one_hot))  # <class '__main__.Activations.one_hot.<locals>.OneHot'>

    """

    def __init__(self, configs: Optional[Dict[str, Any]] = None):
        if configs is None:
            configs = {}
        self.configs = configs

    def __getattr__(self, item: str) -> nn.Module:
        kwargs = self.configs.setdefault(item, {})
        try:
            return getattr(nn, item)(**kwargs)
        except AttributeError:
            func = getattr(torch, item, getattr(nn.functional, item, None))
            if func is None:
                raise NotImplementedError(
                    "neither pytorch nor custom Activations "
                    f"implemented activation '{item}'"
                )
            return Lambda(partial(func, **kwargs), item)

    def module(self, name: Optional[str]) -> nn.Module:
        if name is None:
            return nn.Identity()
        return getattr(self, name)

    # publications

    @property
    def glu(self) -> nn.Module:
        config = self.configs.setdefault("glu", {})
        in_dim = config.get("in_dim")
        if in_dim is None:
            raise ValueError("`in_dim` should be provided in glu")
        bias = config.setdefault("bias", True)

        class GLU(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.linear = nn.Linear(in_dim, 2 * in_dim, bias)

            def forward(self, x: torch.Tensor) -> torch.Tensor:
                projection, gate = self.linear(x).chunk(2, dim=1)
                return projection * torch.sigmoid(gate)

        return GLU()

    @property
    def mish(self) -> nn.Module:
        class Mish(nn.Module):
            def forward(self, x: torch.Tensor) -> torch.Tensor:
                return x * (torch.tanh(nn.functional.softplus(x)))

        return Mish()

    # custom

    # TODO : After updated to pytorch>=1.7.0, re-implement this
    @property
    def logit(self) -> nn.Module:
        kwargs = self.configs.setdefault("logit", {})
        eps = kwargs.setdefault("eps", 1.0e-6)

        def _logit(x: torch.Tensor) -> torch.Tensor:
            x = torch.clamp(x, eps, 1.0 - eps)
            return torch.log(x / (1.0 - x))

        return Lambda(_logit, f"logit_{eps:.2e}")

    @property
    def atanh(self) -> nn.Module:
        kwargs = self.configs.setdefault("atanh", {})
        eps = kwargs.setdefault("eps", 1.0e-6)

        def _atanh(x: torch.Tensor) -> torch.Tensor:
            return torch.atanh(torch.clamp(x, -1.0 + eps, 1.0 - eps))

        return Lambda(_atanh, f"atanh_{eps:.2e}")

    @property
    def isoftplus(self) -> nn.Module:
        kwargs = self.configs.setdefault("isoftplus", {})
        eps = kwargs.setdefault("eps", 1.0e-6)

        def _isoftplus(x: torch.Tensor) -> torch.Tensor:
            return torch.log(x.clamp_min(eps).exp() - 1.0)

        return Lambda(_isoftplus, f"isoftplus_{eps:.2e}")

    @property
    def sign(self) -> nn.Module:
        config = self.configs.setdefault("sign", {})
        randomize_at_zero = config.setdefault("randomize_at_zero", False)
        eps = config.setdefault("eps", 1e-12)
        suffix = "_randomized" if randomize_at_zero else ""

        def _core(x: torch.Tensor) -> torch.Tensor:
            if randomize_at_zero:
                x = x + (2 * torch.empty_like(x).uniform_() - 1.0) * eps
            return torch.sign(x)

        return Lambda(_core, f"sign{suffix}")

    @property
    def one_hot(self) -> nn.Module:
        f = lambda x: x * (x == torch.max(x, dim=1, keepdim=True)[0]).to(torch.float32)
        return Lambda(f, "one_hot")

    @property
    def sine(self) -> nn.Module:
        return Lambda(lambda x: torch.sin(x), "sine")

    @property
    def multiplied_sine(self) -> nn.Module:
        class MultipliedSine(_multiplied_activation):
            def _core(self, multiplied: torch.Tensor) -> torch.Tensor:
                return torch.sin(multiplied)

        config = self.configs.setdefault("multiplied_sine", {})
        config.setdefault("ratio", 10.0)
        return MultipliedSine(**config)

    @property
    def multiplied_tanh(self) -> nn.Module:
        class MultipliedTanh(_multiplied_activation):
            def _core(self, multiplied: torch.Tensor) -> torch.Tensor:
                return torch.tanh(multiplied)

        return MultipliedTanh(**self.configs.setdefault("multiplied_tanh", {}))

    @property
    def multiplied_sigmoid(self) -> nn.Module:
        class MultipliedSigmoid(_multiplied_activation):
            def _core(self, multiplied: torch.Tensor) -> torch.Tensor:
                return torch.sigmoid(multiplied)

        return MultipliedSigmoid(**self.configs.setdefault("multiplied_sigmoid", {}))

    @property
    def multiplied_softmax(self) -> nn.Module:
        class MultipliedSoftmax(_multiplied_activation):
            def __init__(self, ratio: float, dim: int = 1, trainable: bool = True):
                super().__init__(ratio, trainable)
                self.dim = dim

            def _core(self, multiplied: torch.Tensor) -> torch.Tensor:
                return nn.functional.softmax(multiplied, dim=self.dim)

        return MultipliedSoftmax(**self.configs.setdefault("multiplied_softmax", {}))

    @property
    def cup_masked(self) -> nn.Module:
        class CupMasked(nn.Module):
            def __init__(
                self,
                bias: float = 2.0,
                ratio: float = 2.0,
                retain_sign: bool = False,
                trainable: bool = True,
            ):
                super().__init__()
                sigmoid_kwargs = {"ratio": ratio, "trainable": trainable}
                self.sigmoid = Activations.make("multiplied_sigmoid", sigmoid_kwargs)
                bias = math.log(math.exp(bias) - 1.0)
                bias_ = torch.tensor([bias], dtype=torch.float32)
                self.bias = bias_ if not trainable else nn.Parameter(bias_)
                self.retain_sign = retain_sign
                self.trainable = trainable

            def forward(self, net: torch.Tensor) -> torch.Tensor:
                net_abs = net.abs()
                bias = nn.functional.softplus(self.bias)
                cup_mask = self.sigmoid(net_abs - bias)
                masked = net_abs * cup_mask
                if not self.retain_sign:
                    return masked
                return masked * torch.sign(net)

            def extra_repr(self) -> str:
                bias_str = f"(bias): {self.bias.item()}"
                positive_str = f"(positive): {not self.retain_sign}"
                trainable_str = f"(trainable): {self.trainable}"
                return f"{bias_str}\n{positive_str}\n{trainable_str}"

        return CupMasked(**self.configs.setdefault("cup_masked", {}))

    @classmethod
    def make(
        cls,
        name: Optional[str],
        config: Optional[Dict[str, Any]] = None,
    ) -> nn.Module:
        if name is None:
            return nn.Identity()
        if config is None:
            config = {}
        if name.startswith("leaky_relu"):
            splits = name.split("_")
            if len(splits) == 3:
                config["negative_slope"] = float(splits[-1])
            config.setdefault("inplace", True)
            return nn.LeakyReLU(**config)
        if name.lower() == "relu":
            name = "ReLU"
            config.setdefault("inplace", True)
        return cls({name: config}).module(name)


class mode_context(context_error_handler):
    """
    Help entering specific mode and recovering previous mode

    This is a context controller for entering specific mode at the beginning
    and back to previous mode at the end.

    Parameters
    ----------
    module : nn.Module, arbitrary PyTorch module.

    Examples
    --------
    >>> module = nn.Module()
    >>> with mode_context(module):
    >>>     pass  # do something

    """

    def __init__(
        self,
        module: nn.Module,
        *,
        to_train: Optional[bool],
        use_grad: Optional[bool],
    ):
        self._to_train = to_train
        self._module, self._training = module, module.training
        self._cache = {p: p.requires_grad for p in module.parameters()}
        if use_grad is not None:
            for p in module.parameters():
                p.requires_grad_(use_grad)
        if use_grad is None:
            self._grad_context: Optional[ContextManager] = None
        else:
            self._grad_context = torch.enable_grad() if use_grad else torch.no_grad()

    def __enter__(self) -> None:
        if self._to_train is not None:
            self._module.train(mode=self._to_train)
        if self._grad_context is not None:
            self._grad_context.__enter__()

    def _normal_exit(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._to_train is not None:
            self._module.train(mode=self._training)
        if self._grad_context is not None:
            self._grad_context.__exit__(exc_type, exc_val, exc_tb)
        for p, v in self._cache.items():
            p.requires_grad_(v)


class train_context(mode_context):
    """
    Useful when we need to get gradients with our PyTorch model during evaluating.
    """

    def __init__(self, module: nn.Module, *, use_grad: bool = True):
        super().__init__(module, to_train=True, use_grad=use_grad)


class eval_context(mode_context):
    """
    Useful when we need to predict something with our PyTorch model during training.
    """

    def __init__(self, module: nn.Module, *, use_grad: bool = False):
        super().__init__(module, to_train=False, use_grad=use_grad)


__all__ = [
    "is_int",
    "is_float",
    "to_standard",
    "to_torch",
    "to_numpy",
    "to_2d",
    "to_prob",
    "collate_np_dicts",
    "collate_tensor_dicts",
    "switch_requires_grad",
    "get_gradient",
    "scheduler_requires_metric",
    "parse_uri",
    "to_relative",
    "parse_args",
    "parse_path",
    "inject_mlflow_stuffs",
    "summary",
    "Lambda",
    "LoggingMixinWithRank",
    "Initializer",
    "Activations",
    "mode_context",
    "train_context",
    "eval_context",
]
