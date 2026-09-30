from fastapi import FastAPI, UploadFile, File
from app.services.vision import analyze_image
import shutil
import os

app = FastAPI(
    title="SnapAssist",
    description="On-device multimodal AI assistant",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "project": "SnapAssist",
        "status": "running",
        "message": "SnapAssist backend is working!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze-image")
async def analyze_uploaded_image(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(file_path)

    return result