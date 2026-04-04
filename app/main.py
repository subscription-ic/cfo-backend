from fastapi import FastAPI
from app.api.v1.endpoints import document

app = FastAPI(title="Backend API")

app.include_router(document.router, prefix="/api/v1/documents", tags=["documents"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
