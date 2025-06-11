import os
print(os.path.exists(r"C:/Users/nagas/deepfake-detection/audio/saved_models/final_model.keras"))
print(os.path.exists(r"C:/Users/nagas/deepfake-detection/video/saved_models_video/final_resnet50_deepfake.keras"))

from app.models.video_model import video_model
print(video_model.predict)  # Should show a method object
