import os
import platform
from pathlib import Path

class Settings:
    def __init__(self):
        # Detect if running in WSL/Linux
        self.IS_WSL = "microsoft" in platform.uname().release.lower()
        
        if self.IS_WSL:
            # Linux-style paths (WSL)
            self.VIDEO_MODEL_PATH = Path("/mnt/c/Users/nagas/deepfake-detection/videocdf/saved_models_video/faceforensics_models/final_faceforensics_resnet50.keras")
            self.AUDIO_MODEL_PATH = Path("/mnt/c/Users/nagas/deepfake-detection/audio/saved_models/final_model.keras")
        else:
            # Native Windows paths
            self.VIDEO_MODEL_PATH = Path(r"C:/Users/nagas/deepfake-detection/videocdf/saved_models_video/faceforensics_models/final_resnet50_deepfake.keras")
            self.AUDIO_MODEL_PATH = Path(r"C:/Users/nagas/deepfake-detection/audio/saved_models/final_model.keras")

        # Processing parameters
        self.FRAME_INTERVAL = 10
        self.INPUT_SHAPE = (224, 224, 3)
        self.AUDIO_SAMPLE_RATE = 16000
        self.N_MFCC = 40
        
        # Thresholds
        self.VIDEO_THRESHOLD = 0.65
        self.AUDIO_THRESHOLD = 0.70
        
        # Temp storage
        self.TEMP_DIR = Path(os.getenv("TEMP_DIR", "temp_uploads"))

settings = Settings()
