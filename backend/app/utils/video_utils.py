import cv2
import numpy as np
from pathlib import Path
from app.config import settings

def extract_frames(video_path: Path):
    frames = []
    vidcap = cv2.VideoCapture(str(video_path))
    
    try:
        count = 0
        while vidcap.isOpened():
            success, frame = vidcap.read()
            if not success:
                break
            
            if count % settings.FRAME_INTERVAL == 0:
                frame = cv2.resize(frame, settings.INPUT_SHAPE[:2])
                frames.append(frame)
            count += 1
    finally:
        vidcap.release()

        # Debug prints
    print(f"Extracted {len(frames)} frames")
    if len(frames) > 0:
        print(f"Frame shape: {frames[0].shape}")
        print(f"Frame data type: {frames[0].dtype}")
        print(f"Frame value range: {frames[0].min()} to {frames[0].max()}")
    
    return np.array(frames)
