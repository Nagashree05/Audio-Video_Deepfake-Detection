import os
import cv2
from mtcnn import MTCNN
from tqdm import tqdm
import argparse

class BaseVideoProcessor:
    def __init__(self, checkpoint_file="processed_videos.log"):
        self.checkpoint_file = checkpoint_file
        
    def extract_faces_from_video(video_path, output_dir, frames_per_video=30):
        """Extract faces from video frames using MTCNN face detection."""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Failed to open video: {video_path}")
                return 0

            detector = MTCNN()
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Calculate frame indices to sample
            frame_indices = []
            if total_frames > 0:
                frame_indices = sorted(list(
                    {int(total_frames * (i / frames_per_video)) 
                    for i in range(frames_per_video)}
                ))
            else:
                print(f"Warning: {video_path} has 0 frames. Skipping.")
                return 0

            saved_count = 0
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue

                # Detect faces
                faces = detector.detect_faces(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if faces:
                    # Get largest face
                    main_face = max(faces, key=lambda x: x['confidence'])
                    x, y, w, h = main_face['box']
                    
                    # Ensure coordinates are within frame boundaries
                    x, y = max(0, x), max(0, y)
                    face = frame[y:y+h, x:x+w]
                    
                    if face.size == 0:
                        continue

                    # Save face
                    resized = cv2.resize(face, (224, 224))
                    img_name = f"{uuid.uuid4()}.jpg"
                    output_path = os.path.join(output_dir, img_name)
                    
                    if cv2.imwrite(output_path, resized):
                        saved_count += 1
                    else:
                        print(f"Failed to save image: {output_path}")

            cap.release()
            return saved_count

        except Exception as e:
            print(f"Error processing {video_path}: {str(e)}")
            return 0

def load_processed_videos():
    """Load set of already processed videos from checkpoint file."""
    if not os.path.exists(CHECKPOINT_FILE):
        return set()
    with open(CHECKPOINT_FILE, 'r') as f:
        return set(line.strip() for line in f)