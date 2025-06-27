from pydantic import BaseModel
from typing import Optional

class DetectionRequest(BaseModel):
    pass  # Empty as we're using file upload

class DetectionResult(BaseModel):
    video_confidence: Optional[float] = None
    audio_confidence: Optional[float] = None
    is_fake: bool
