import torch
import torch.nn as nn

from typing import *
from functools import partial
from torch.nn.functional import softplus

from ..types import tensor_dict_type


class BN(nn.BatchNorm1d):
    def forward(self, net: torch.Tensor) -> torch.Tensor:
        if len(net.shape) == 3:
            net = net.transpose(1, 2)
        net = super().forward(net)
        if len(net.shape) == 3:
            net = net.transpose(1, 2)
        return net


class Dropout(nn.Module):
    def __init__(self, dropout: float):
        if dropout < 0.0 or dropout >= 1.0:
            msg = f"dropout probability has to be between [0, 1), but got {dropout}"
            raise ValueError(msg)
        super().__init__()
        self._keep_prob = 1.0 - dropout
        self._mask_cache: Optional[torch.Tensor] = None

    def forward(self, net: torch.Tensor, *, reuse: bool = False) -> torch.Tensor:
        if not self.training or self._keep_prob >= 1.0 - 1.0e-8:
            return net
        if reuse:
            mask = self._mask_cache
        else:
            self._mask_cache = mask = (
                torch.bernoulli(net.new(*net.shape).fill_(self._keep_prob))
                / self._keep_prob
            )
        net = net * mask
        del mask
        return net

    def extra_repr(self) -> str:
        return f"keep={self._keep_prob}"


class EMA(nn.Module):
    def __init__(
        self,
        decay: float,
        named_parameters: List[Tuple[str, nn.Parameter]],
    ):
        super().__init__()
        self._decay = decay
        self._named_parameters = named_parameters
        for name, param in self.tgt_params:
            self.register_buffer(self.get_name(True, name), param.data.clone())
            self.register_buffer(self.get_name(False, name), param.data.clone())

    @staticmethod
    def get_name(train: bool, name: str) -> str:
        prefix = "tr" if train else "ema"
        return f"{prefix}_{name}"

    @property
    def tgt_params(self) -> Iterator[Tuple[str, nn.Parameter]]:
        return map(
            lambda pair: (pair[0].replace(".", "_"), pair[1]),
            self._named_parameters,
        )

    def forward(self) -> None:
        for name, param in self.tgt_params:
            setattr(self, self.get_name(True, name), param.data.clone())
            ema_name = self.get_name(False, name)
            ema_attr = getattr(self, ema_name)
            ema = (1.0 - self._decay) * param.data + self._decay * ema_attr
            setattr(self, ema_name, ema.clone())

    def train(self, mode: bool = True) -> "EMA":
        super().train(mode)
        for name, param in self.tgt_params:
            param.data = getattr(self, self.get_name(mode, name)).clone()
        return self

    def extra_repr(self) -> str:
        max_str_len = max(len(name) for name, _ in self.tgt_params)
        return "\n".join(
            [f"(0): decay_rate={self._decay}\n(1): Params("]
            + [
                f"  {name:<{max_str_len}s} - torch.Tensor({list(param.shape)})"
                for name, param in self.tgt_params
            ]
            + [")"]
        )


class MTL(nn.Module):
    def __init__(
        self,
        num_tasks: int,
        method: Optional[str] = None,
    ):
        super().__init__()
        self._n_task, self._method = num_tasks, method
        if method is None or method == "naive":
            pass
        elif method == "softmax":
            self.w = torch.nn.Parameter(torch.ones(num_tasks))
        else:
            raise NotImplementedError(f"MTL method '{method}' not implemented")
        self.registered = False
        self._slice: Optional[int] = None
        self._registered: Dict[str, int] = {}

    def register(self, names: List[str]) -> None:
        if self.registered:
            raise ValueError("re-register is not permitted")
        self._rev_registered = {}
        for name in sorted(names):
            idx = len(self._registered)
            self._registered[name], self._rev_registered[idx] = idx, name
        self._slice, self.registered = len(names), True
        if self._slice > self._n_task:
            raise ValueError("registered names are more than n_task")

    def forward(
        self,
        loss_dict: tensor_dict_type,
        naive: bool = False,
    ) -> torch.Tensor:
        if not self.registered:
            raise ValueError("losses need to be registered")
        if naive or self._method is None:
            return self._naive(loss_dict)
        return getattr(self, f"_{self._method}")(loss_dict)

    @staticmethod
    def _naive(loss_dict: tensor_dict_type) -> torch.Tensor:
        return sum(loss_dict.values())  # type: ignore

    def _softmax(self, loss_dict: tensor_dict_type) -> torch.Tensor:
        assert self._slice is not None
        w = self.w if self._slice == self._n_task else self.w[: self._slice]
        softmax_w = nn.functional.softmax(w, dim=0)
        losses = []
        for key, loss in loss_dict.items():
            idx = self._registered.get(key)
            losses.append(loss if idx is None else loss * softmax_w[idx])
        final_loss: torch.Tensor = sum(losses)  # type: ignore
        return final_loss * self._slice

    def extra_repr(self) -> str:
        method = "naive" if self._method is None else self._method
        return f"n_task={self._n_task}, method='{method}'"


class Pruner(nn.Module):
    def __init__(self, config: Dict[str, Any], w_shape: Optional[List[int]] = None):
        super().__init__()
        self.eps: torch.Tensor
        self.exp: torch.Tensor
        self.alpha: Union[torch.Tensor, nn.Parameter]
        self.beta: Union[torch.Tensor, nn.Parameter]
        self.gamma: Union[torch.Tensor, nn.Parameter]
        self.max_ratio: Union[torch.Tensor, nn.Parameter]
        tensor = partial(torch.tensor, dtype=torch.float32)
        self.method = config.setdefault("method", "auto_prune")
        if self.method == "surgery":
            if w_shape is None:
                msg = "`w_shape` of `Pruner` should be provided when `surgery` is used"
                raise ValueError(msg)
            self.register_buffer("mask", torch.ones(*w_shape, dtype=torch.float32))
            self.register_buffer("alpha", tensor([config.setdefault("alpha", 1.0)]))
            self.register_buffer("beta", tensor([config.setdefault("beta", 4.0)]))
            self.register_buffer("gamma", tensor([config.setdefault("gamma", 1e-4)]))
            self.register_buffer("eps", tensor([config.setdefault("eps", 1e-12)]))
            keys = ["alpha", "beta", "gamma", "eps"]
        elif self.method == "simplified":
            self.register_buffer("alpha", tensor([config.setdefault("alpha", 0.01)]))
            self.register_buffer("beta", tensor([config.setdefault("beta", 1.0)]))
            self.register_buffer(
                "max_ratio", tensor([config.setdefault("max_ratio", 1.0)])
            )
            self.register_buffer("exp", tensor([config.setdefault("exp", 0.5)]))
            keys = ["alpha", "beta", "max_ratio", "exp"]
        else:
            self.register_buffer(
                "alpha",
                tensor(
                    [
                        config.setdefault(
                            "alpha", 1e-4 if self.method == "hard_prune" else 1e-2
                        )
                    ]
                ),
            )
            self.register_buffer("beta", tensor([config.setdefault("beta", 1.0)]))
            self.register_buffer("gamma", tensor([config.setdefault("gamma", 1.0)]))
            self.register_buffer(
                "max_ratio", tensor([config.setdefault("max_ratio", 1.0)])
            )
            if not all(
                scalar > 0
                for scalar in [self.alpha, self.beta, self.gamma, self.max_ratio]
            ):
                raise ValueError("parameters should greater than 0. in pruner")
            self.register_buffer("eps", tensor([config.setdefault("eps", 1e-12)]))
            if self.method == "auto_prune":
                for attr in ["alpha", "beta", "gamma", "max_ratio"]:
                    setattr(self, attr, torch.log(torch.exp(getattr(self, attr)) - 1))
                self.alpha, self.beta, self.gamma, self.max_ratio = map(
                    lambda param: nn.Parameter(param),
                    [self.alpha, self.beta, self.gamma, self.max_ratio],
                )
            keys = ["alpha", "beta", "gamma", "max_ratio", "eps"]
        self._repr_keys = keys

    def forward(self, w: torch.Tensor) -> torch.Tensor:
        w_abs = torch.abs(w)
        if self.method == "surgery":
            mu, std = torch.mean(w_abs), torch.std(w_abs)
            zeros_mask = self.mask == 0.0
            ones_mask = self.mask == 1.0
            to_zeros_mask = ones_mask & (w_abs <= 0.9 * (mu - self.beta * std))  # type: ignore
            to_ones_mask = zeros_mask & (w_abs >= 1.1 * (mu + self.beta * std))  # type: ignore
            self.mask.masked_fill(to_zeros_mask, 0.0)  # type: ignore
            self.mask.masked_fill(to_ones_mask, 1.0)  # type: ignore
            mask = self.mask
            del mu, std, ones_mask, zeros_mask, to_zeros_mask, to_ones_mask
        else:
            if self.method != "auto_prune":
                alpha, beta, ratio = self.alpha, self.beta, self.max_ratio
            else:
                alpha, beta, ratio = map(
                    softplus, [self.alpha, self.beta, self.max_ratio]
                )
            if self.method == "simplified":
                log_w = torch.min(ratio, beta * torch.pow(w_abs, self.exp))
            else:
                w_abs_mean = torch.mean(w_abs)
                gamma = (
                    self.gamma if self.method != "auto_prune" else softplus(self.gamma)
                )
                log_w = torch.log(torch.max(self.eps, w_abs / (w_abs_mean * gamma)))
                log_w = torch.min(ratio, beta * log_w)
                del w_abs_mean
            mask = torch.max(alpha / beta * log_w, log_w)
            del log_w
        w = w * mask
        del w_abs, mask
        return w

    def extra_repr(self) -> str:
        if self.method == "auto_prune":
            return f"method='{self.method}'"
        max_str_len = max(map(len, self._repr_keys))
        return "\n".join(
            [f"(0): method={self.method}\n(1): Settings("]
            + [
                f"  {key:<{max_str_len}s} - {getattr(self, key).item()}"
                for key in self._repr_keys
            ]
            + [")"]
        )


__all__ = ["BN", "Dropout", "EMA", "MTL", "Pruner"]
