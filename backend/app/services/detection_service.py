import threading
from pathlib import Path
from app.config import settings
from app.models.video_model import video_model
from app.models.audio_model import audio_model
from app.utils import video_utils, audio_utils

class DetectionService:
    def __init__(self):
        self.temp_dir = settings.TEMP_DIR
        self.temp_dir.mkdir(exist_ok=True)

    def process_video(self, video_path: Path):
        results = {"video_confidence": None}

        try:
            frames = video_utils.extract_frames(video_path)
            results["video_confidence"] = video_model.predict(frames)
        except Exception as e:
            raise RuntimeError(f"Video processing failed: {str(e)}")

        return results

    def process_audio(self, media_path: Path):
        results = {"audio_confidence": None}
        audio_path = self.temp_dir / "audio.wav"

        try:
            audio_utils.extract_audio(media_path, audio_path)
            if audio_path.exists():
                results["audio_confidence"] = audio_model.predict(audio_path)
                audio_path.unlink()  # Clean up after prediction
            else:
                print("Audio file not created")
        except Exception as e:
            print(f"Audio processing failed: {e}")
            results["audio_confidence"] = None

        return results

    def process_upload(self, video_path: Path):
        """
        Deprecated in new main.py but kept for compatibility.
        Processes both video and audio in parallel.
        """
        results = {"video_confidence": None, "audio_confidence": None}

        def video_task():
            try:
                frames = video_utils.extract_frames(video_path)
                results["video_confidence"] = video_model.predict(frames)
            except Exception as e:
                raise RuntimeError(f"Video processing failed: {str(e)}")

        def audio_task():
            try:
                audio_path = self.temp_dir / "audio.wav"
                audio_utils.extract_audio(video_path, audio_path)
                if audio_path.exists():
                    results["audio_confidence"] = audio_model.predict(audio_path)
                    audio_path.unlink()
                else:
                    print("Audio file not created")
            except Exception as e:
                print(f"Audio processing failed: {e}")
                results["audio_confidence"] = None

        v_thread = threading.Thread(target=video_task)
        a_thread = threading.Thread(target=audio_task)

        v_thread.start()
        a_thread.start()
        v_thread.join()
        a_thread.join()

        return results
