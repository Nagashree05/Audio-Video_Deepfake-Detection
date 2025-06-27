import numpy as np
from app.models.audio_model import audio_model  # Adjust import if needed

# List of test audio files (replace with your paths)
test_files = [
    "/mnt/c/Users/nagas/deepfake-detection/temp_uploads/r1.wav",
    "/mnt/c/Users/nagas/deepfake-detection/temp_uploads/r2.wav"
]

for file_path in test_files:
    try:
        score = audio_model.predict(file_path)
        print(f"File: {file_path} | Model output: {score:.4f}")
        # Interpret the result (assuming 0 = fake, 1 = real; adjust for your model)

        if score > 0.5:
            print("Prediction: REAL\n")
        else:
            print("Prediction: FAKE\n")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
