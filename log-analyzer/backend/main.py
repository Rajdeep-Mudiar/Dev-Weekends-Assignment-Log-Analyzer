from fastapi import FastAPI, UploadFile, File
import shutil

from parser import parse_line
from analyzer import analyze, get_ai_insights
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    try:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logs = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parsed, typ = parse_line(line)
                logs.append((parsed, typ))

        # Get basic analysis
        results = analyze(logs)
        
        # Get AI insights
        results["insights"] = await get_ai_insights(results)
        
        return results
    finally:
        if os.path.exists(path):
            os.remove(path)