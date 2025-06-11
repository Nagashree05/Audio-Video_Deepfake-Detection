import numpy as np
import cv2
from app.models.video_model import video_model  # Adjust import if needed

def extract_frames(video_path, frame_interval=10):
    frames = []
    vidcap = cv2.VideoCapture(video_path)
    count = 0
    while vidcap.isOpened():
        success, frame = vidcap.read()
        if not success:
            break
        if count % frame_interval == 0:
            frame = cv2.resize(frame, (224, 224))
            frames.append(frame)
        count += 1
    vidcap.release()
    return np.array(frames)

# Path to your test video
test_video_path = "/mnt/c/Users/nagas/deepfake-detection/temp_uploads/upsc.mp4"  

# Extract and preprocess frames
frames = extract_frames(test_video_path)
print(f"Extracted {len(frames)} frames.")

if len(frames) == 0:
    print("No frames extracted. Check your video file.")
else:
    # Run prediction
    score = video_model.predict(frames)
    print(f"Model output (mean confidence): {score:.4f}")
    # Interpret the result (adjust threshold according to your model)
    if score > 0.5:
        print("Prediction: FAKE")
    else:
        print("Prediction: REAL")
