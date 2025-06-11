from pydantic import BaseModel

class DetectionRequest(BaseModel):
    pass  # Empty as we're using file upload

class DetectionResult(BaseModel):
    video_confidence: float
    audio_confidence: float | None
    is_fake: bool
