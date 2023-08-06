from typing import Any
from typing import Dict

from ....configs import Configs


@Configs.register("rnn", "default")
class DefaultRNNConfig(Configs):
    def get_default(self) -> Dict[str, Any]:
        return {
            "cell": "GRU",
            "num_layers": 1,
            "cell_config": {
                "batch_first": True,
                "hidden_size": 256,
            },
        }


__all__ = ["DefaultRNNConfig"]
