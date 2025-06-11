import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
class CelebDFConfig(Config):
    DATASET_NAME = "celebdf"
    DATA_DIR = os.path.join(Config.BASE_DIR, "data", "datasets", "celebdf")
    MODEL_DIR = os.path.join(Config.BASE_DIR, "saved_models_video", "celebdf_models")
    
class FaceForensicsConfig(Config):
    DATASET_NAME = "faceforensics"
    DATA_DIR = os.path.join(Config.BASE_DIR, "data", "datasets", "faceforensics")
    MODEL_DIR = os.path.join(Config.BASE_DIR, "saved_models_video", "faceforensics_models")
    PRETRAINED_MODEL = os.path.join(Config.BASE_DIR, "models", "celebdf_models", "final_resnet50_deepfake.h5")
