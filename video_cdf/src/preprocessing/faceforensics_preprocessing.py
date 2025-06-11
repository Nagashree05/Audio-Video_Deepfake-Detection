from .base_preprocessing import BaseVideoProcessor

class FaceForensicsProcessor(BaseVideoProcessor):
    def __init__(self):
        super().__init__("data/datasets/faceforensics/processed_videos.log")
    
    def process_faceforensics_dataset(self):
        """Process FaceForensics++ dataset structure"""
        base_dir = "data/datasets/faceforensics/raw_videos/FFPP_Data"
        
        # Define paths
        real_videos_dir = os.path.join(base_dir, "original_sequences", "youtube", "c23", "videos")
        fake_videos_dir = os.path.join(base_dir, "manipulated_sequences", "Deepfakes", "c23", "videos")
        
        # Output directories
        real_output_dir = "data/datasets/faceforensics/processed/real"
        fake_output_dir = "data/datasets/faceforensics/processed/fake"
        
        os.makedirs(real_output_dir, exist_ok=True)
        os.makedirs(fake_output_dir, exist_ok=True)
        
        print("Processing real videos...")
        self.process_video_directory(real_videos_dir, real_output_dir)
        
        print("Processing fake videos...")
        self.process_video_directory(fake_videos_dir, fake_output_dir)