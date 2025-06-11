import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.saving import register_keras_serializable
from app.config import settings

@register_keras_serializable()
def focal_loss_fixed(y_true, y_pred, gamma=2.0, alpha=0.25):
    epsilon = 1e-8
    y_pred = tf.clip_by_value(y_pred, epsilon, 1. - epsilon)
    cross_entropy = -y_true * tf.math.log(y_pred)
    loss = alpha * tf.pow(1. - y_pred, gamma) * cross_entropy
    return tf.reduce_mean(tf.reduce_sum(loss, axis=1))

class VideoModel:
    def __init__(self):
        self.model = load_model(
            settings.VIDEO_MODEL_PATH,
            custom_objects={'focal_loss_fixed': focal_loss_fixed}
        )
        
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
