import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
import json

# DB Config
DB_URL = os.getenv("DB_CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost:5432/tallydb")
engine = create_engine(DB_URL)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim

# Chunking config
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def embed_and_store(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    chunks = text_splitter.split_text(raw_text)
    embeddings = model.encode(chunks, show_progress_bar=True)

    document_id = str(uuid.uuid4())

    with engine.begin() as conn:
        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            conn.execute(
                text("""
                    INSERT INTO document_chunks (document_id, content, embedding, metadata)
                    VALUES (:doc_id, :content, :embedding, :metadata)
                """),
                {
                    "doc_id": document_id,
                    "content": chunk,
                    "embedding": vector.tolist(),
                    "metadata": json.dumps({"filename": os.path.basename(file_path), "chunk_index": i})
                }
            )

    print(f"✅ Inserted {len(chunks)} chunks from {file_path} into Postgres.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python embed.py <path_to_text_file>")
        exit(1)
    embed_and_store(sys.argv[1])
