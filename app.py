from fastapi import FastAPI
from search_engine.engine import SearchEngine
from typing import List,Dict, Any
from fastapi import HTTPException

app=FastAPI()
engine = SearchEngine()

# health endpoint
@app.get("/")
def root():
  return {"status": "running"}

@app.post("/documents")#create
def add_document(document: Dict[str, Any]):
  doc_id = engine.index_document(document)
  return {
    "message": "Document indexed successfully",
    "doc_id": doc_id
  }

@app.get("/documents/{doc_id}")
def get_document(doc_id: int):
  try:
    return engine.get_document(doc_id)
  except KeyError as e:
    raise HTTPException(
      status_code=404,
      detail=str(e)
    )


@app.post("/documents/batch")#batch ingestion
def add_documents(documents: List[Dict[str, Any]]):
  doc_ids = engine.index_documents(documents)
  return {
      "count": len(doc_ids),
      "doc_ids": doc_ids
  }

@app.put("/documents/{doc_id}")#update
def update_document(doc_id: int, document: dict):
  try:
    engine.update_document(doc_id, document)
    return {
      "message": "Document updated successfully"
    }
  except KeyError as e:
    raise HTTPException(
      status_code=404,
      detail=str(e)
    )

@app.delete("/documents/{doc_id}")#delete
def delete_document(doc_id: int):
  try:
    engine.delete_document(doc_id)
    return {
      "message":"Document deleted successfully"
    }
  except KeyError as e:
    raise HTTPException(
      status_code=404,
      detail=str(e)
    )

from pydantic import BaseModel
class SearchRequest(BaseModel):query: str

@app.post("/search")
def search(request: SearchRequest):
  try:
    documents = engine.search(request.query)
    return {
      "count": len(documents),
      "documents": documents
    }
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )
@app.post("/search/ids")
def search_ids(request: SearchRequest):
  try:
    ids=engine.search_ids(request.query)
    return {
       "count": len(ids),
      "ids": ids
    }
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )
@app.post("/search/count")
def search_count(request: SearchRequest):
  try:
    bitmap = engine.search_bitmap(request.query)
    return {
      "count": len(bitmap)
    }
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )

class SaveRequest(BaseModel):
    path: str
@app.post("/save")
def save(request: SaveRequest):
    try:
        engine.save(request.path)
        return {"message": "Index saved successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

class LoadRequest(BaseModel):
    path: str
@app.post("/load")
def load(request: LoadRequest):
    global engine
    try:
        engine = SearchEngine.load(request.path)
        return {"message": "Index loaded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
