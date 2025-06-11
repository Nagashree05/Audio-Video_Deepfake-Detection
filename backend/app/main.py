from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid
from app.services.detection_service import DetectionService
from app.schemas import DetectionResult
from app.config import settings
import traceback

app = FastAPI()
detection_service = DetectionService()

@app.post("/detect", response_model=DetectionResult)
async def detect_deepfake(video: UploadFile = File(...)):
    # Ensure temp directory exists
    settings.TEMP_DIR.mkdir(exist_ok=True)

    # Sanitize and uniquify filename to avoid issues with spaces or collisions
    safe_filename = f"{uuid.uuid4().hex}_{video.filename.replace(' ', '_')}"
    temp_video = settings.TEMP_DIR / safe_filename

    try:
        # Save uploaded file
        with temp_video.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # Double-check file was saved
        if not temp_video.exists():
            raise HTTPException(status_code=500, detail="File was not saved correctly.")

        # Process video
        results = detection_service.process_upload(temp_video)

        # Determine final verdict
        is_fake = (
            (results["video_confidence"] is not None and results["video_confidence"] > settings.VIDEO_THRESHOLD)
            or
            (results["audio_confidence"] is not None and results["audio_confidence"] > settings.AUDIO_THRESHOLD)
        )

        return {
            "video_confidence": results["video_confidence"],
            "audio_confidence": results["audio_confidence"],
            "is_fake": is_fake
        }

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Only delete the file, not the whole directory (safer for concurrent requests)
        if temp_video.exists():
            temp_video.unlink()
