from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="RAG QA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """占位上传端点，后续实现：保存文件、抽取文本、入库"""
    contents = await file.read()
    # 临时文件保存
    os.makedirs("/tmp/uploads", exist_ok=True)
    path = f"/tmp/uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "path": path}
