import os
import shutil

from typing import *
from torch import Tensor
from cftool.misc import shallow_copy_dict
from cftool.misc import LoggingMixin
from cftool.ml.utils import register_metric
from cfdata.tabular.processors.base import Processor

from ..modules import *
from ..types import tensor_dict_type
from ..losses import LossBase
from ..configs import configs_dict
from ..configs import Configs
from ..misc.toolkit import Initializer
from ..models.base import model_dict
from ..models.base import ModelBase
from ..models.base import SiameseModelBase
from ..modules.heads import head_dict
from ..modules.heads import HeadBase
from ..modules.heads import HeadConfigs
from ..modules.extractors import ExtractorBase
from ..modules.aggregators import AggregatorBase
from ..modules.extractors.base import extractor_dict


def register_initializer(name: str) -> Callable[[Callable], Callable]:
    def _register(f: Callable) -> Callable:
        Initializer.add_initializer(f, name)
        return f

    return _register


def register_processor(name: str) -> Callable[[Type], Type]:
    return Processor.register(name)


def register_loss(name: str) -> Callable[[Type], Type]:
    return LossBase.register(name)


def register_extractor(name: str) -> Callable[[Type], Type]:
    return ExtractorBase.register(name)


def register_head(name: str) -> Callable[[Type], Type]:
    return HeadBase.register(name)


def register_aggregator(name: str) -> Callable[[Type], Type]:
    return AggregatorBase.register(name)


class PipeInfo(NamedTuple):
    key: str
    transform: str = "default"
    extractor: Optional[str] = None
    reuse_extractor: bool = True
    head: Optional[str] = None
    extractor_config: str = "default"
    head_config: str = "default"
    extractor_meta_scope: Optional[str] = None
    head_meta_scope: Optional[str] = None


def register_pipe(
    key: str,
    *,
    transform: str = "default",
    extractor: Optional[str] = None,
    reuse_extractor: bool = True,
    head: Optional[str] = None,
    extractor_config: str = "default",
    head_config: str = "default",
    extractor_meta_scope: Optional[str] = None,
    head_meta_scope: Optional[str] = None,
) -> Callable[[Type], Type]:
    return ModelBase.register_pipe(
        key,
        transform=transform,
        extractor=extractor,
        head=head,
        extractor_config=extractor_config,
        reuse_extractor=reuse_extractor,
        head_config=head_config,
        extractor_meta_scope=extractor_meta_scope,
        head_meta_scope=head_meta_scope,
    )


def register_model(
    name: str,
    *,
    pipes: Optional[List[PipeInfo]] = None,
) -> Optional[Callable[[Type], Type]]:
    if pipes is None:
        return ModelBase.register(name)

    @ModelBase.register(name)
    class _(ModelBase):
        pass

    for pipe in pipes:
        _ = register_pipe(**pipe._asdict())(_)  # type: ignore

    return None


def register_siamese_model(
    name: str,
    *,
    pipes: Optional[List[PipeInfo]] = None,
) -> Optional[Callable[[Type], Type]]:
    if pipes is None:
        return SiameseModelBase.register(name)

    @SiameseModelBase.register(name)
    class _(SiameseModelBase):
        pass

    for pipe in pipes:
        _ = register_pipe(**pipe._asdict())(_)  # type: ignore

    return None


def _register_config(
    base: Type[Configs],
    scope: str,
    name: str,
    config: Optional[Dict[str, Any]] = None,
) -> Optional[Callable[[Type], Type]]:
    if config is None:
        return base.register(scope, name)

    def register(config_: Dict[str, Any]) -> None:
        @base.register(scope, name)
        class _(base):  # type: ignore
            def get_default(self) -> Dict[str, Any]:
                return shallow_copy_dict(config_)

    register(config)
    return None


def register_config(
    scope: str,
    name: str,
    *,
    config: Optional[Dict[str, Any]] = None,
) -> Optional[Callable[[Type], Type]]:
    return _register_config(Configs, scope, name, config)  # type: ignore


def register_head_config(
    scope: str,
    name: str,
    *,
    head_config: Optional[Dict[str, Any]] = None,
) -> Optional[Callable[[Type], Type]]:
    return _register_config(HeadConfigs, scope, name, head_config)  # type: ignore


api_root = os.path.abspath(os.path.dirname(__file__))
external_root = os.path.join(api_root, os.pardir, "external_")
external_root = os.path.abspath(external_root)
external_init_file = os.path.join(external_root, "__init__.py")


def _get_external_files() -> List[str]:
    files = []
    for file in sorted(os.listdir(external_root)):
        if not os.path.isfile(os.path.join(external_root, file)):
            continue
        if file == "__init__.py":
            continue
        if os.path.splitext(file)[1] != ".py":
            continue
        files.append(file)
    return files


def _refresh_external_init() -> None:
    with open(external_init_file, "w") as f:
        for file in _get_external_files():
            f.write(f"from .{os.path.splitext(file)[0]} import *\n")


def register_external(file_path: str) -> None:
    file = os.path.basename(file_path)
    tgt_path = os.path.join(external_root, file)
    if os.path.isfile(tgt_path):
        print(
            f"{LoggingMixin.warning_prefix}'{file}' already registered, "
            "it will be overwritten."
        )
    shutil.copy(file_path, tgt_path)
    _refresh_external_init()
    import cflearn
    import importlib

    importlib.reload(cflearn)
    importlib.reload(cflearn.external_)
    exec(f"importlib.reload(cflearn.external_.{os.path.splitext(file)[0]})")


def remove_external(file_path: str) -> None:
    file = os.path.basename(file_path)
    tgt_path = os.path.join(external_root, file)
    if not os.path.isfile(tgt_path):
        raise ValueError(f"'{file}' is not registered")
    os.remove(tgt_path)
    _refresh_external_init()


def remove_all_external() -> None:
    for file in _get_external_files():
        remove_external(os.path.join(external_root, file))


def register_module(name: str, module_base: Any) -> None:
    current_extractor = extractor_dict.pop(name, None)
    current_head = head_dict.pop(name, None)
    current_model = model_dict.pop(name, None)
    if current_extractor is not None:
        print(
            f"{LoggingMixin.warning_prefix}'{name}' already exists in "
            f"`extractor_dict`, it will be overwritten"
        )
    if current_head is not None:
        print(
            f"{LoggingMixin.warning_prefix}'{name}' already exists in `head_dict`, "
            "it will be overwritten"
        )
    if current_model is not None:
        print(
            f"{LoggingMixin.warning_prefix}'{name}' already exists in `model_dict`, "
            "it will be overwritten"
        )

    @register_head(name)
    class _(HeadBase):
        def __init__(self, in_dim: int, out_dim: int, **kwargs: Any):
            super().__init__(in_dim, out_dim, **kwargs)
            self.model = module_base(in_dim, out_dim, **kwargs)

        def forward(self, net: Tensor) -> Union[Tensor, tensor_dict_type]:
            return self.model(net)

    current_config = configs_dict.get(name, {}).pop("default", None)
    if current_config is not None:
        print(
            f"{LoggingMixin.warning_prefix}'{name}' already exists in "
            f"`configs_dict`, it will be overwritten"
        )
    register_head_config(name, "default", head_config={})
    register_model(name, pipes=[PipeInfo(name, extractor="identity_ts")])


__all__ = [
    "register_extractor",
    "register_head",
    "register_aggregator",
    "register_pipe",
    "register_model",
    "register_siamese_model",
    "register_config",
    "register_head_config",
    "register_metric",
    "register_optimizer",
    "register_scheduler",
    "register_initializer",
    "register_processor",
    "register_loss",
    "register_external",
    "remove_external",
    "remove_all_external",
    "register_module",
    "Initializer",
    "Processor",
    "LossBase",
    "PipeInfo",
]
