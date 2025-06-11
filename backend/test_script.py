# Test script
from app.models.video_model import video_model
import cv2
import numpy as np

# Load a known real video and test
test_video = "C:/Users/nagas/deepfake-detection/temp_uploads/fake1.mp4"
vidcap = cv2.VideoCapture(test_video)
frames = []

for i in range(10):  # Test with 10 frames
    ret, frame = vidcap.read()
    if ret:
        frame = cv2.resize(frame, (224, 224))
        frames.append(frame)

frames = np.array(frames)
confidence = video_model.predict(frames)
print(f"Confidence for known real video: {confidence}")
