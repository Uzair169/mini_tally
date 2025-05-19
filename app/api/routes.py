from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.core.rag import process_query
from app.core.embeddings import embed_and_store

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/ask")
async def ask(query_request: QueryRequest):
    try:
        result = await process_query(query_request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        success = embed_and_store(content.decode("utf-8"), file.filename)
        if not success:
            raise HTTPException(status_code=500, detail="Embedding failed")
        return {"status": "uploaded and embedded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing failed: {str(e)}")
