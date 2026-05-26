from fastapi import FastAPI, UploadFile, File
import shutil

from parser import parse_line
from analyzer import analyze

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    path = f"temp_{file.filename}"

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    logs = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parsed, typ = parse_line(line)
            logs.append((parsed, typ))

    return analyze(logs)