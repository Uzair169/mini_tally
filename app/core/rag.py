# app/core/rag.py

from app.core.embeddings import get_vectorstore, embed_query
from app.core.model_router import generate_answer

def process_chunks(docs):
    return "\n".join([doc.page_content for doc in docs])

async def process_query(query: str):
    vectorstore = get_vectorstore()
    embedded_query = embed_query(query)
    # Correct: pass only the embedded vector and k
    docs = vectorstore.similarity_search_by_vector(embedded_query, k=5)
    context = process_chunks(docs)

    prompt = f"""Answer the following question using the context below.

Context:
{context}

Question: {query}

Respond in JSON with fields:
- net_income
- revenue
- period
"""
    return generate_answer(prompt)
