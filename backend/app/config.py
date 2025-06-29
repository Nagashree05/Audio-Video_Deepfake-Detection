import os
import platform
from pathlib import Path
from huggingface_hub import hf_hub_download

class Settings:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        
        # Model filenames on HF repo
        repo_id = "nagashreens05/deepguard"

        # Download models from HF (they will be cached in ~/.cache/huggingface)
        self.VIDEO_MODEL_PATH = Path(
            hf_hub_download(repo_id=repo_id, filename="final_faceforensics_resnet50.keras")
        )

        self.VIDEO_MODEL_CDF_PATH = Path(
            hf_hub_download(repo_id=repo_id, filename="final_resnet50_deepfake.keras")
        )

        self.AUDIO_MODEL_PATH = Path(
            hf_hub_download(repo_id=repo_id, filename="final_model.keras")
        )

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
