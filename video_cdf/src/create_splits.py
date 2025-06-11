import os
import pandas as pd

# Ensure the base directory exists
base_dir = '/mnt/c/Users/nagas/deepfake-detection/video_cdf/data/datasets/faceforensics/splits'
os.makedirs(base_dir, exist_ok=True)

def get_image_paths(directory):
    if not os.path.exists(directory):
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

splits = ['train', 'val', 'test']

for split in splits:
    real_folder = os.path.join(base_dir, split, 'real')
    fake_folder = os.path.join(base_dir, split, 'fake')
    real_files = get_image_paths(real_folder)
    fake_files = get_image_paths(fake_folder)
    # Correct label assignment!
    filepaths = real_files + fake_files
    labels = [0] * len(real_files) + [1] * len(fake_files)
    df = pd.DataFrame({
        'filepath': filepaths,
        'label': labels
    })
    csv_path = os.path.join(base_dir, f'{split}.csv')
    df.to_csv(csv_path, index=False)
    print(f"Created {csv_path} with {len(df)} samples")

# Optional: Print first few rows for verification
for split in splits:
    csv_path = os.path.join(base_dir, f'{split}.csv')
    if os.path.exists(csv_path):
        print(f"\nFirst rows of {csv_path}:")
        print(pd.read_csv(csv_path).head())
