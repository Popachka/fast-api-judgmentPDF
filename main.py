import os

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.models.pdf_file import PDFFiles
from app.config import get_db_url

app = FastAPI()
print(get_db_url())
app.add_middleware(DBSessionMiddleware, db_url=get_db_url())

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)