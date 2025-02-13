from llama_cpp import Llama
import sys
import os

sys.path.append("../littleSeven/")
from common.config import cfg

from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler


llm = Llama(model_path=cfg.llm_gguf_model_path, verbose=False)


template = """Question: {question}

Answer: Tell me things you know"""

# replace the placeholder {question} with the real content.
prompt = PromptTemplate.from_template(template)


# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


llm = LlamaCpp(
    model_path=cfg.llm_gguf_model_path,
    n_gpu_layers=1,  # Use m2 max chip, metal sets to 1.
    n_batch=512,
    n_ctx=4096,
    f16_kv=True,
    callback_manager=callback_manager,
    stop=["Question:"],
    verbose=False,
)

question = """
Question: do you know machine learning?
"""
llm.invoke(question)