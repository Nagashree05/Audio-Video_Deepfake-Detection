import os
import platform
from pathlib import Path

class Settings:
    def __init__(self):
        # Detect if running in WSL/Linux
        self.IS_WSL = "microsoft" in platform.uname().release.lower()

        BASE_DIR = Path(__file__).resolve().parent
        
        self.VIDEO_MODEL_PATH = BASE_DIR / "trained_models/final_faceforensics_resnet50.keras"
        self.VIDEO_MODEL_CDF_PATH = BASE_DIR / "trained_models/video_final_resnet50_deepfake.keras"
        self.AUDIO_MODEL_PATH = BASE_DIR / "trained_models/audio_final_model.keras"


        # self.VIDEO_MODEL_PATH = Path("/trained_models/video_final_faceforensics_resnet50.keras")
        # self.VIDEO_MODEL_CDF_PATH = Path("/trained_models/video_final_resnet50_deepfake.keras")
        # self.AUDIO_MODEL_PATH = Path("/trained_models/audio_final_model.keras")

        # Processing parameters
        self.FRAME_INTERVAL = 10
        self.INPUT_SHAPE = (224, 224, 3)
        self.AUDIO_SAMPLE_RATE = 16000
        self.N_MFCC = 40

        # Thresholds
        self.VIDEO_THRESHOLD = 0.4
        self.AUDIO_THRESHOLD = 0.4

        # Temp storage
        self.TEMP_DIR = Path(os.getenv("TEMP_DIR", "temp_uploads")).resolve()
        self.TEMP_DIR.mkdir(exist_ok=True)

settings = Settings()
