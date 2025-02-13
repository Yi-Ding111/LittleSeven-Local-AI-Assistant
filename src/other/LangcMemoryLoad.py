import sys
import json
import os

sys.path.append("../littleSeven/src/")
from common.config import cfg

MEMORY_FILE = cfg.memory_file_path


def load_memory(memory):
    """
    load langchain history memory from local
    Params:
        memory: memory = ConversationBufferMemory(...)
    """
    import time

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)

                saved_timestamp = data.get("timestamp", 0)
                current_time = time.time()
                elapsed_time = current_time - saved_timestamp
                if elapsed_time > 24 * 3600:
                    return

                messages = data.get("messages", [])
                for message in messages:
                    if message["role"] == "human":
                        memory.chat_memory.add_user_message(message["content"])
                    elif message["role"] == "ai":
                        memory.chat_memory.add_ai_message(message["content"])

            except json.JSONDecodeError as e:
                return f"Cannot load history. {e}"
