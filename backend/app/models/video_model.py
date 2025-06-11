import numpy as np
from tensorflow.keras.models import load_model
from app.config import settings

class VideoModel:
    def __init__(self):
        self.model = load_model(settings.VIDEO_MODEL_PATH)
        
    def predict(self, frames):
        print(f"🔍 DEBUG - Input frames shape: {frames.shape}")
        print(f"🔍 DEBUG - Input frames dtype: {frames.dtype}")
        print(f"🔍 DEBUG - Input frames range: {frames.min()} to {frames.max()}")
        
        # Normalize frames
        if frames.dtype != np.float32:
            frames = frames.astype('float32')
        
        if frames.max() > 1.0:
            frames = frames / 255.0
            
        print(f"🔍 DEBUG - After preprocessing range: {frames.min()} to {frames.max()}")
        
        # Get raw predictions
        raw_predictions = self.model.predict(frames)
        print(f"🔍 DEBUG - Raw model output: {raw_predictions}")
        print(f"🔍 DEBUG - Raw predictions shape: {raw_predictions.shape}")
        
        # Check what your model actually outputs
        if raw_predictions.shape[1] == 2:  # Binary classification with 2 outputs
            fake_probability = raw_predictions[:, 1].mean()  # Probability of "fake"
            print(f"🔍 DEBUG - Fake probability: {fake_probability}")
            return fake_probability
        else:
            result = raw_predictions.mean()
            print(f"🔍 DEBUG - Mean prediction: {result}")
            return result

video_model = VideoModel()
