from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate,
)

import sys

sys.path.append("../littleSeven/src/")
from common.config import cfg





system_message=SystemMessagePromptTemplate.from_template(
    """ You are an AI assistant. Your responses will be converted into speech.
        Please ensure that your answers:
        - Are conversational and sound natural when spoken.
        - Use a friendly and engaging tone.
        - Avoid overly formal or robotic language.
        - Use contractions where appropriate (e.g., "I'm" instead of "I am").
        - Keep sentences short and easy to understand.
        - Use a storytelling style when possible.
        
        Respond to the human as helpfully and accurately as possible."""
)

history_placeholder=MessagesPlaceholder(variable_name="history",optional=True)

scratchpad_placeholder = MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)

human_message=HumanMessagePromptTemplate.from_template(
    """
        Classify the question as normal, operations or retriever: {input}.

        normal:
        -Ask the time.
        -Daily greetings.
        -Random Querstions.

        operations:
        -Open some applications.
        -Write some notes.
        -find some files.

        retriever:
        -Conclude information form local knowledge.
        -Information from my laptap.
        -Where the corresponding file path on my laptop.

        You need to ensure that you response the quesntion with 2 parts:
        First part: choose one from these choices: 'normal', 'operations' or 'retriever'.
        Second part: re-write the question with the history memory as a reference in clear sentences.
        Use - to concatenate these 2 parts
    
    (reminder to respond in a JSON blob no matter what)"""
)

assisstant_message=AIMessagePromptTemplate.from_template(
    "Understood! I will analyze your question type and provide a detailed response."
)


prompt_template_classification=ChatPromptTemplate.from_messages([
    system_message,
    history_placeholder,
    human_message,
    assisstant_message
])

def get_prompt_classification():
    return prompt_template_classification