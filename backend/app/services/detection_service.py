import threading
from pathlib import Path
from app.config import settings
from app.models.video_model import video_model
from app.models.audio_model import audio_model
from app.utils import video_utils, audio_utils

class DetectionService:
    def __init__(self):
        self.temp_dir = Path('temp_uploads')

    def process_upload(self, video_path: Path):
        # Create temp directory
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize results
        results = {"video_confidence": None, "audio_confidence": None}
        
        # Video processing thread
        def video_task():
            try:
                frames = video_utils.extract_frames(video_path)
                results["video_confidence"] = video_model.predict(frames)
            except Exception as e:
                raise RuntimeError(f"Video processing failed: {str(e)}")

        # Audio processing thread
        def audio_task():
            try:
                audio_path = self.temp_dir / "audio.wav"
                audio_utils.extract_audio(video_path, audio_path)
                if audio_path.exists():
                    results["audio_confidence"] = audio_model.predict(audio_path)
                else:
                    print("Audio file not created")
                    results["audio_confidence"] = None
            except Exception as e:
                print(f"Audio processing failed: {e}")
                results["audio_confidence"] = None

        # Run threads
        v_thread = threading.Thread(target=video_task)
        a_thread = threading.Thread(target=audio_task)
        
        v_thread.start()
        a_thread.start()
        
        v_thread.join()
        a_thread.join()

        # Cleanup
        if video_path.exists():
            video_path.unlink()
            
        return results
