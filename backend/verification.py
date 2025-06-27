import os
print(os.path.exists(r"C:/Users/nagas/deepfake-detection/audio/saved_models/final_model.keras"))
print(os.path.exists(r"C:/Users/nagas/deepfake-detection/videocdf/saved_models_video/faceforensics_models/final_faceforensics_resnet50.keras"))

from app.models.video_model import video_model
print(video_model.predict)  # Should show a method object
