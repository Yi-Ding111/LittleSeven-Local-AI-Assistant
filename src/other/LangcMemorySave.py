import sys
import json
import os

sys.path.append("../littleSeven/src/")
from common.config import cfg

MEMORY_FILE = cfg.memory_file_path


def save_memory(memory):
    """
    save langchain memory to local
    Params:
        memory: memory = ConversationBufferMemory(...)
    """
    import time

    timestamp = time.time()

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

    messages_as_dicts = [
        {"role": msg.type, "content": msg.content}
        for msg in memory.chat_memory.messages
    ]

    data_to_save = {"timestamp": timestamp, "messages": messages_as_dicts}

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data_to_save, file, ensure_ascii=False, indent=4)
