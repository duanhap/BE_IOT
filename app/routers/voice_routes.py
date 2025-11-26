from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import whisper
import numpy as np
import wave
import os
import uuid
from app.services.voice_history_service import VoiceHistoryService
from app.database.database import get_db
from sqlalchemy.orm import Session

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Session storage to track current audio file
current_session = {"filename": None}

print("Đang load Whisper...")
model = whisper.load_model("tiny")
print("Whisper ready!")

router = APIRouter(prefix="/voice", tags=["Voice Handler"])

@router.post('/chunk')
async def chunk(request: Request):
    # Nhận raw binary data từ request body
    data = await request.body()
    
    if not data:
        raise HTTPException(status_code=400, detail="No data")

    # Initialize session if needed
    if current_session["filename"] is None:
        current_session["filename"] = str(uuid.uuid4()) + ".raw"

    raw_path = os.path.join(UPLOAD_FOLDER, current_session["filename"])
    with open(raw_path, "ab") as f:
        f.write(data)

    return {"message": "OK", "session": current_session["filename"]}

@router.post('/finalize')
async def finalize(db: Session = Depends(get_db)):
    voice_history_service = VoiceHistoryService(db)
          
    if current_session["filename"] is None:
        raise HTTPException(status_code=400, detail="no audio session")

    raw_path = os.path.join(UPLOAD_FOLDER, current_session["filename"])
    if not os.path.exists(raw_path):
        raise HTTPException(status_code=400, detail="raw file missing")

    # Đọc file raw
    with open(raw_path, "rb") as f:
        raw_data = f.read()

    print(f"[SERVER] Processing audio file: {current_session['filename']}, size: {len(raw_data)} bytes")

    # gọi service - để language=None để service tự detect
    result = voice_history_service.process_voice(
        raw_data=raw_data,
        language=None  # Service sẽ tự detect
    )

    # Xóa file tạm và reset session
    try:
        os.remove(raw_path)
    except:
        pass
    current_session["filename"] = None

    return result
# Thêm endpoint để debug session
@router.get("/session")
async def get_session():
    return {
        "current_session": current_session["filename"],
        "session_exists": current_session["filename"] is not None
    }