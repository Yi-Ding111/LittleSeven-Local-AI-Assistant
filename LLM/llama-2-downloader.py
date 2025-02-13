from llama_cpp import Llama

import sys
import os

common_path = "../littleSeven/"
if common_path not in sys.path:
    sys.path.append(common_path)

from common.config import cfg

# download .gguf llama-2 model from huggingface
llama2 = Llama.from_pretrained(
    repo_id=cfg.model_name_llama_gguf,
    filename=cfg.file_name_llama_gguf,
    verbose=False,
    local_dir=cfg.model_path_gguf,
)
