import sys
sys.path.append('.')
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid
import mimetypes
import traceback

from backend.app.services.detection_service import DetectionService
from backend.app.schemas import DetectionResult
from backend.app.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
detection_service = DetectionService()

sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent.parent))

origins = [
    "http://localhost:3000",  # Your frontend URL
    "http://127.0.0.1:3000",  # Sometimes React uses this
    "http://localhost", 
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect", response_model=DetectionResult)
async def detect_deepfake(file: UploadFile = File(...)):
    # Ensure temp directory exists
    settings.TEMP_DIR.mkdir(exist_ok=True)

    # Sanitize and uniquify filename
    safe_filename = f"{uuid.uuid4().hex}_{file.filename.replace(' ', '_')}"
    temp_file_path = settings.TEMP_DIR / safe_filename

    try:
        # Save uploaded file
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Confirm file saved correctly
        if not temp_file_path.exists():
            raise HTTPException(status_code=500, detail="File was not saved correctly.")

        # Detect file type from MIME
        mime_type, _ = mimetypes.guess_type(str(temp_file_path))

        if mime_type is None:
            raise HTTPException(status_code=400, detail="Could not determine file type.")

        # Dispatch to correct service
        if mime_type.startswith("video"):
            results = detection_service.process_video(temp_file_path)
        elif mime_type.startswith("audio"):
            results = detection_service.process_audio(temp_file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload a valid audio or video file.")

        # Final fake detection verdict
        is_fake = (
            (results.get("video_confidence") is not None and results["video_confidence"] > settings.VIDEO_THRESHOLD)
            or
            (results.get("audio_confidence") is not None and results["audio_confidence"] > settings.AUDIO_THRESHOLD)
        )

        return {
            "video_confidence": results.get("video_confidence"),
            "audio_confidence": results.get("audio_confidence"),
            "is_fake": is_fake
        }

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

    finally:
        if temp_file_path.exists():
            temp_file_path.unlink()

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
