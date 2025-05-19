import os
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import DB_CONNECTION_STRING

EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "local")  # "openai" or "local"

if EMBEDDING_BACKEND == "openai":
    EMBEDDING_MODEL = OpenAIEmbeddings()
else:
    EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    return PGVector(
        connection_string=DB_CONNECTION_STRING,
        embedding_function=EMBEDDING_MODEL,
        collection_name="tally_docs"
    )

def embed_and_store(text, source):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([text])
    for c in chunks:
        c.metadata = {"source": source}
    vectorstore = get_vectorstore()
    # Pass embedding model explicitly here
    vectorstore.add_documents(chunks, embedding=EMBEDDING_MODEL)
    return True

def embed_query(query):
    return EMBEDDING_MODEL.embed_query(query)
