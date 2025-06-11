import os
import numpy as np
import librosa
import hashlib
from tqdm import tqdm
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Configuration
DATASET_PATHS = {
    'for-2sec': '/mnt/c/Users/nagas/deepfake-detection/audio/data/for-2sec',
    'for-norm': '/mnt/c/Users/nagas/deepfake-detection/audio/data/for-norm',
    'for-original': '/mnt/c/Users/nagas/deepfake-detection/audio/data/for-original',
    'for-rerec': '/mnt/c/Users/nagas/deepfake-detection/audio/data/for-rerec'
}
PROCESSED_DIR = 'processed_audio_data'
SR = 16000
N_MFCC = 40
MAX_LENGTH = 100

os.makedirs(PROCESSED_DIR, exist_ok=True)

def load_audio(file_path):
    try:
        y, _ = librosa.load(file_path, sr=SR)
        if len(y) < SR:
            y = np.pad(y, (0, SR - len(y)))
        return y
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def augment_audio(y):
    if random.random() < 0.5:
        y += np.random.normal(0, 0.005, len(y))
    if random.random() < 0.5:
        y = librosa.effects.pitch_shift(y, sr=SR, n_steps=np.random.uniform(-2, 2))
    if random.random() < 0.5:
        rate = np.random.uniform(0.8, 1.2)
        y = librosa.effects.time_stretch(y, rate=rate)
    return y

def extract_features(file_path, augment=False):
    y = load_audio(file_path)
    if y is None:
        return None
    
    if augment:
        y = augment_audio(y)
    
    mfcc = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=N_MFCC)
    if mfcc.shape[1] < MAX_LENGTH:
        mfcc = np.pad(mfcc, ((0,0), (0, MAX_LENGTH - mfcc.shape[1])))
    else:
        mfcc = mfcc[:, :MAX_LENGTH]
    
    return mfcc.T

def process_dataset():
    all_features = []
    all_labels = []
    seen_hashes = set()
    
    for dataset_name, base_path in DATASET_PATHS.items():
        print(f"\nProcessing {dataset_name} dataset...")
        
        for split in ['training', 'validation', 'testing']:
            for label in ['real', 'fake']:
                dir_path = os.path.join(base_path, split, label)
                if not os.path.exists(dir_path):
                    continue
                    
                label_idx = 0 if label == 'real' else 1
                
                for file in tqdm(os.listdir(dir_path), desc=f"{split}/{label}"):
                    file_path = os.path.join(dir_path, file)
                    
                    if not file.lower().endswith('.wav'):
                        continue
                        
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    if file_hash in seen_hashes:
                        continue
                    seen_hashes.add(file_hash)
                    
                    augment = (split == 'training')
                    features = extract_features(file_path, augment=augment)
                    
                    if features is not None:
                        all_features.append(features)
                        all_labels.append(label_idx)

    # Convert to arrays
    X = np.array(all_features)
    y = np.array(all_labels)
    
    # Train/Val/Test split
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )
    
    # Normalization
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
    X_val = scaler.transform(X_val.reshape(-1, X_val.shape[-1])).reshape(X_val.shape)
    X_test = scaler.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)
    
    # Save processed data
    np.save(os.path.join(PROCESSED_DIR, 'X_train.npy'), X_train)
    np.save(os.path.join(PROCESSED_DIR, 'X_val.npy'), X_val)
    np.save(os.path.join(PROCESSED_DIR, 'X_test.npy'), X_test)
    np.save(os.path.join(PROCESSED_DIR, 'y_train.npy'), y_train)
    np.save(os.path.join(PROCESSED_DIR, 'y_val.npy'), y_val)
    np.save(os.path.join(PROCESSED_DIR, 'y_test.npy'), y_test)
    joblib.dump(scaler, os.path.join(PROCESSED_DIR, 'scaler.joblib'))
    
    print(f"\nData shapes after preprocessing:")
    print(f"Train: {X_train.shape}")
    print(f"Validation: {X_val.shape}")
    print(f"Test: {X_test.shape}")
    print(f"Saved processed data to {PROCESSED_DIR}")

if __name__ == "__main__":
    process_dataset()
