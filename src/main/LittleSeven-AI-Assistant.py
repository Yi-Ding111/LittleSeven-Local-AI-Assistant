import webrtcvad
import os
import sys


sys.path.append("../littleSeven/src/")
from common.config import cfg

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, Tool

from langchain.memory import ConversationBufferMemory
from langchain.agents import (
    AgentExecutor,
    create_structured_chat_agent,
)
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from langchain.schema.output_parser import StrOutputParser

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from other.FontCustomize import colored_text
from other.LangcMemoryLoad import load_memory
from other.LangcMemorySave import save_memory

from text_speech_conversion.SpeechToText import STT
from text_speech_conversion.TextToSpeech import text_to_speech_offline

from langc_tools.LocalTime import get_local_time
from langc_tools.ChromeSearch import google_chrome_search_tool
from langc_tools.LocalFileOpen import open_file
from langc_tools.NoteCreate import create_stickies_note
from langc_tools.LocalFireRag import get_rag_retriever


from prompt_template.PromptDaily import get_daily_prompt
from prompt_template.PromptLaptopOperation import get_laptop_operation_prompt
from prompt_template.RagPromptContext import get_contextualize_prompt
from prompt_template.RagPromptDocChain import get_qa_prompt
from prompt_template.PromptRag import get_prompt_rag
from prompt_template.PromptBranchClassification import get_prompt_classification


memory = ConversationBufferMemory(
    memory_key=cfg.history_placeholder_variable, return_messages=True
)

llm = ChatOpenAI(model=cfg.LLM_model)


## ======================= daily chat agent ======================= ##

tools = [
    Tool(
        name="LocalTime",
        func=get_local_time,
        description="Use this tool to get the current local time.",
    )
]

agent_normal_chat = create_structured_chat_agent(
    llm=llm, tools=tools, prompt=get_daily_prompt()
)

agent_executor_normal_chat = AgentExecutor(
    agent=agent_normal_chat,
    tools=tools,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)


## ======================= local operations agent ======================= ##

laptop_operations_tools = [
    Tool(
        name="CreateNote",
        func=create_stickies_note,
        description="Use this tool to write down a note",
    ),
    Tool(
        name="GoogleChromeSearch",
        func=google_chrome_search_tool,
        description="Use this tool to search some web pages through google if asking you search something online",
    ),
    Tool(
        name="OpenLocalPath",
        func=open_file,
        description="Use this tool to open the local file.",
    ),
]

agent_laptop_operations = create_structured_chat_agent(
    llm=llm, tools=laptop_operations_tools, prompt=get_laptop_operation_prompt()
)

agent_executor_laptop_operations = AgentExecutor(
    agent=agent_laptop_operations,
    tools=laptop_operations_tools,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)


## ======================= rag retriever agent ======================= ##

# reformulate the question based on chat history
history_aware_retriever = create_history_aware_retriever(
    llm=llm, retriever=get_rag_retriever(), prompt=get_contextualize_prompt()
)

# Create a chain for passing a list of Documents to a model.
# feeds all retrieved context into the LLM
qa_chain = create_stuff_documents_chain(llm=llm, prompt=get_qa_prompt())

# First use history_aware_retriever to adjust the problem (complete historical information)
# Then use retriever to query the knowledge base.
# Finally, the query result is passed to question_answer_chain to generate the final answer.
rag_chain = create_retrieval_chain(
    retriever=history_aware_retriever, combine_docs_chain=qa_chain
)


rag_tools = [
    Tool(
        name="Answer Question with local knowledge",
        func=lambda input, **kwargs: rag_chain.invoke(
            {
                "input": input,
                "history": memory.chat_memory.messages,
                "agent_scratchpad": "",
            }
        ),
        description="Use RAG to answer questions based on retrieved knowledge on local laptop.",
    )
]


agent_rag = create_structured_chat_agent(
    llm=llm, tools=rag_tools, prompt=get_prompt_rag()
)

agent_executor_rag = AgentExecutor(
    agent=agent_rag,
    tools=rag_tools,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)


## ======================= langchain branching ======================= ##

branches = RunnableBranch(
    (
        lambda x: "normal" in x.get("input", "").lower(),
        RunnableLambda(lambda x: agent_executor_normal_chat.invoke(x)),
    ),
    (
        lambda x: "operations" in x.get("input", "").lower(),
        RunnableLambda(lambda x: agent_executor_laptop_operations.invoke(x)),
    ),
    (
        lambda x: "retriever" in x.get("input", "").lower(),
        RunnableLambda(
            lambda x: agent_executor_rag.invoke(
                {"input": x["input"], "history": memory.chat_memory.messages}
            )
        ),
    ),
    RunnableLambda(lambda x: {"output": "I didn't understand your request."}),
)


classification_chain = get_prompt_classification() | llm | StrOutputParser()


classification_runnable = RunnableLambda(
    lambda x: {
        "history": memory.chat_memory.add_user_message(x["input"])
        or memory.chat_memory.messages,
        "input": classification_chain.invoke(
            {"input": x["input"], "history": memory.chat_memory.messages}
        ),
    }
)

chain = classification_runnable | branches


if __name__ == "__main__":
    stt = STT()

    # load local history memory
    load_memory(memory)


    while True:
        user_input = input("YD: ").strip()  # remove spaces

        if user_input.lower() == "exit":
            # close PyAudio resource
            stt.close()
            # save history memory locally
            save_memory(memory)

            break

        elif user_input == "":  # User presses the Enter key
            # speech to text
            input_audio = stt.record_audio()
            plain_text = stt.transcribe_audio(input_audio=input_audio)

            print(colored_text(plain_text, "34", bold=True))

            result = chain.invoke({"input": plain_text})

            # print("LittleSeven: ", result['output'])
            print(colored_text(f"LittleSeven: {result['output']}", "34", bold=True))

            # text to speech
            text_to_speech_offline(result["output"])
        
        else: 
            print(colored_text(user_input, "34", bold=True))

            result = chain.invoke({"input": user_input})

            print(colored_text(f"LittleSeven: {result['output']}", "34", bold=True))