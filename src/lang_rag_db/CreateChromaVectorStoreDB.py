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


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # open pdf file
    text = ""
    for page in doc:  # recursive each page
        text += page.get_text("text") + "\n"  # Extract text and wrap
    return text.strip()


# extract text from pdf
pdf_text = extract_text_from_pdf(cfg.fire_dir_origin)


def create_vector_store(
    text: str,
    metadata: str,
    chunk_size: int = cfg.chunk_size,
    chunk_overlap: int = cfg.chunk_overlap,
    embedding_model_name: str = cfg.embedding_model_name,
):
    # combine text content and file metadata together
    documents = [Document(page_content=pdf_text, metadata={"source": metadata})]

    # Splits text into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(documents)

    # Define the embedding model
    embeddings = OpenAIEmbeddings(model=embedding_model_name)

    # create chroma db
    db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)

    return db


db = create_vector_store(text=pdf_text, metadata=cfg.fire_dir_with_notes)


