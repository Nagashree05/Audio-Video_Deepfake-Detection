# test_models.py
from app.models.video_model import video_model
from app.models.audio_model import audio_model

print("=== MODEL SUMMARIES ===")
print("Video model output shape:", video_model.model.output_shape)
print("Audio model output shape:", audio_model.model.output_shape)

# Test with dummy data
import numpy as np

# Test video model
dummy_frames = np.random.rand(5, 224, 224, 3) * 255  # 5 random frames
video_result = video_model.predict(dummy_frames)
print(f"Video model test result: {video_result}")

# Check if your models expect different label encoding
print("\n=== MODEL OUTPUT INTERPRETATION ===")
print("Check if your model outputs:")
print("- [prob_real, prob_fake] or")
print("- Single value where 0=real, 1=fake")
