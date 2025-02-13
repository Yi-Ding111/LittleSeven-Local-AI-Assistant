from dotenv import load_dotenv
import os
import sys
import fitz
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

sys.path.append("../littleSeven/src/")
from common.config import cfg

load_dotenv()


db_dir = os.path.join(os.getcwd(), "src","db")
persistent_directory = os.path.join(db_dir, "chroma_db")

# Define the embedding model
embeddings = OpenAIEmbeddings(model=cfg.embedding_model_name)

# Load create chroma vecstore with the corresponding embedding function
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)

# create rag retriever
retriever = db.as_retriever(
    search_type=cfg.rag_db_retriever_search_type,
    search_kwargs={"k": cfg.rag_db_retriever_K},
)



def get_rag_retriever():

    return retriever