import sys
import os

common_path = '../littleSeven/'
if common_path not in sys.path:
    sys.path.append(common_path)

from common.config import cfg

from transformers import GPT2LMHeadModel, GPT2Tokenizer

# download model and tokenizer
model = GPT2LMHeadModel.from_pretrained(cfg.model_name)
tokenizer = GPT2Tokenizer.from_pretrained(cfg.model_name)

# save model
model.save_pretrained(cfg.model_path)
tokenizer.save_pretrained(cfg.model_path)