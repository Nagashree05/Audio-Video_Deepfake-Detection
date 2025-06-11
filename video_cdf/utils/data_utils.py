import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight

def ensure_dir(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_splits(data_dir, splits_dir, test_size=0.3, val_size=0.5, random_state=42):
    """Create train/val/test splits from processed data."""
    real_dir = os.path.join(data_dir, "real")
    fake_dir = os.path.join(data_dir, "fake")
    
    ensure_dir(splits_dir)

    # Collect real and fake image paths
    real_images = [os.path.join(real_dir, f) for f in os.listdir(real_dir) 
                  if f.endswith(('.jpg', '.jpeg', '.png'))]
    fake_images = [os.path.join(fake_dir, f) for f in os.listdir(fake_dir) 
                  if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Create DataFrame
    df = pd.DataFrame({
        'filepath': real_images + fake_images,
        'label': [0]*len(real_images) + [1]*len(fake_images)
    })

    # Stratified split
    train_df, temp_df = train_test_split(
        df, 
        test_size=test_size, 
        stratify=df['label'], 
        random_state=random_state,
    )
    val_df, test_df = train_test_split(
        temp_df, 
        test_size=val_size, 
        stratify=temp_df['label'], 
        random_state=random_state,
    )

    # Save splits
    train_df.to_csv(os.path.join(splits_dir, "train.csv"), index=False)
    val_df.to_csv(os.path.join(splits_dir, "val.csv"), index=False)
    test_df.to_csv(os.path.join(splits_dir, "test.csv"), index=False)

    return train_df, val_df, test_df

def create_splits_faceforensics(data_dir="data/datasets/faceforensics/processed", 
                               splits_dir="data/datasets/faceforensics/splits"):
    """Create splits specifically for FaceForensics++ dataset."""
    return create_splits(data_dir, splits_dir)

def load_and_validate_splits(splits_dir):
    """Load and validate train/val/test splits."""
    train_df = pd.read_csv(os.path.join(splits_dir, 'train.csv'))
    val_df = pd.read_csv(os.path.join(splits_dir, 'val.csv'))
    test_df = pd.read_csv(os.path.join(splits_dir, 'test.csv'))
    
    # Validate file paths
    for df, name in zip([train_df, val_df, test_df], ['Train', 'Validation', 'Test']):
        if df.empty:
            raise ValueError(f"{name} DataFrame is empty!")
        if 'filepath' not in df.columns or 'label' not in df.columns:
            raise ValueError(f"{name} DataFrame missing required columns!")
            
        # Fix path separators
        df['filepath'] = df['filepath'].str.replace('\\', '/')
        
        # Filter missing files
        initial_count = len(df)
        df = df[df['filepath'].apply(os.path.exists)].copy()
        removed = initial_count - len(df)
        if removed > 0:
            print(f"Removed {removed} missing files from {name} set")
    
    # Convert labels to strings for Keras compatibility
    train_df['label'] = train_df['label'].astype(str)
    val_df['label'] = val_df['label'].astype(str)
    test_df['label'] = test_df['label'].astype(str)
    
    return train_df, val_df, test_df

def get_class_weights(train_df):
    """Calculate class weights for handling imbalanced datasets."""
    class_weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_df['label']),
        y=train_df['label']
    )
    return dict(enumerate(class_weights))

def print_class_distribution(train_df, val_df, test_df):
    """Print class distribution across splits."""
    print("\nClass distribution:")
    print("Train:", train_df['label'].value_counts())
    print("Validation:", val_df['label'].value_counts())
    print("Test:", test_df['label'].value_counts())
