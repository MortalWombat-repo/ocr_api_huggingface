from fastapi import FastAPI, UploadFile, File
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import io

app = FastAPI()

# Initialize PaddleOCR (lightweight model)
ocr = PaddleOCR(use_angle_cls=True, lang='latin', use_gpu=False)

@app.get("/")
def root():
    return {"message": "PaddleOCR FastAPI is running!"}

@app.post("/ocr")
async def recognize_text(file: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Convert and run OCR
    result = ocr.ocr(np.array(image), cls=True)

    # Extract text lines
    lines = [line[1][0] for line in result[0]]
    return {"text": lines}
