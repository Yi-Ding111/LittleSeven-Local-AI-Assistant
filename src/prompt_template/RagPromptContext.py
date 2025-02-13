from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

import sys

sys.path.append("../littleSeven/src/")
from common.config import cfg


system_message=SystemMessagePromptTemplate.from_template(
    """ Given the following conversation and the input question, rephrase the input question to be a standalone question.

        Provide only ONE action per $JSON_BLOB, as shown:
        ```
        {{
        "action": $TOOL_NAME,
        "action_input": $INPUT
        }}
        ```
        Follow this format:

        Question: input question to answer
        Thought: consider previous and subsequent steps
        Action:
        ```
        $JSON_BLOB
        ```
        Observation: action result
        ... (repeat Thought/Action/Observation N times)
        Thought: I know what to respond
        Action:
        ```
        {{
        "action": "Final Answer",
        "action_input": "Final response to human"
        }}
        ```        
        Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
     
        """    
)

history_placeholder = MessagesPlaceholder(
    variable_name=cfg.history_placeholder_variable, optional=True
)

human_message=HumanMessagePromptTemplate.from_template(
    """{input}
    
    {agent_scratchpad}
    """
)


contextualize_prompt=ChatPromptTemplate.from_messages([
    system_message,
    history_placeholder,
    human_message
])


def get_contextualize_prompt():
    return contextualize_prompt
