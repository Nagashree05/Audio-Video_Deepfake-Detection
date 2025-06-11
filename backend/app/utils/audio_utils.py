import subprocess
from pathlib import Path

def extract_audio(video_path: Path, output_path: Path):
    print(f"🔍 DEBUG - Extracting audio from: {video_path}")
    print(f"🔍 DEBUG - Output audio path: {output_path}")
    
    try:
        command = [
            "ffmpeg",
            "-i", str(video_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"🔍 DEBUG - FFmpeg command succeeded")
        print(f"🔍 DEBUG - Audio file exists: {output_path.exists()}")
        
        if output_path.exists():
            print(f"🔍 DEBUG - Audio file size: {output_path.stat().st_size} bytes")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")
        print(f"❌ FFmpeg stderr: {e.stderr}")
        raise
    except Exception as e:
        print(f"❌ Audio extraction failed: {e}")
        raise
