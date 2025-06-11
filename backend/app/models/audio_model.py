from tensorflow.keras.models import load_model
from app.config import settings
import numpy as np
import librosa

class AudioModel:
    def __init__(self):
        self.model = load_model(settings.AUDIO_MODEL_PATH)
        
    def predict(self, audio_path):
        y, sr = librosa.load(audio_path, sr=settings.AUDIO_SAMPLE_RATE)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=settings.N_MFCC)
        mfcc = mfcc.T  # Now shape: (time_steps, 40)

        # Pad/truncate to 100 time steps
        if mfcc.shape[0] < 100:
            mfcc = np.pad(mfcc, ((0, 100 - mfcc.shape[0]),(0, 0)))
        else:
            mfcc = mfcc[:100, :]
    
        mfcc = np.expand_dims(mfcc, axis=(0, -1))  # Add batch and channel dims
        return self.model.predict(mfcc)[0][0]

audio_model = AudioModel()
