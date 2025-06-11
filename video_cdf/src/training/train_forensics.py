import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import callbacks
import pandas as pd
import numpy as np
from sklearn.utils import class_weight
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from models.resnet_models import build_enhanced_model, create_transfer_model
from utils.data_utils import load_and_validate_splits, get_class_weights
from utils.evaluation_utils import evaluate_model_comprehensive

# Load your data splits
train_df = pd.read_csv('/mnt/c/Users/nagas/deepfake-detection/video_cdf/data/datasets/faceforensics/splits/train.csv')
val_df = pd.read_csv('/mnt/c/Users/nagas/deepfake-detection/video_cdf/data/datasets/faceforensics/splits/val.csv')
test_df = pd.read_csv('/mnt/c/Users/nagas/deepfake-detection/video_cdf/data/datasets/faceforensics/splits/test.csv')

# Convert labels to strings
train_df['label'] = train_df['label'].astype(str)
val_df['label'] = val_df['label'].astype(str)
test_df['label'] = test_df['label'].astype(str)

# Check class distribution
print("Class distribution in FaceForensics++:")
print("Train:", train_df['label'].value_counts())
print("Validation:", val_df['label'].value_counts())
print("Test:", test_df['label'].value_counts())

# Enhanced data augmentation for better generalization
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.15,
    zoom_range=0.15,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    channel_shift_range=20,
    fill_mode='reflect',
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input
)

val_test_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input
)

# Create generators
train_gen = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col='filepath',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=True,
    seed=42
)

val_gen = val_test_datagen.flow_from_dataframe(
    dataframe=val_df,
    x_col='filepath',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=False
)

# Focal Loss to handle class imbalance
def focal_loss(gamma=2., alpha=0.25):
    def focal_loss_fixed(y_true, y_pred):
        epsilon = tf.keras.backend.epsilon()
        y_pred = tf.clip_by_value(y_pred, epsilon, 1. - epsilon)
        p_t = tf.where(tf.equal(y_true, 1), y_pred, 1 - y_pred)
        alpha_factor = tf.ones_like(y_true) * alpha
        alpha_t = tf.where(tf.equal(y_true, 1), alpha_factor, 1 - alpha_factor)
        cross_entropy = -tf.math.log(p_t)
        weight = alpha_t * tf.pow((1 - p_t), gamma)
        loss = weight * cross_entropy
        return tf.reduce_mean(loss)
    return focal_loss_fixed

# Load your pre-trained model and create transfer learning model
model, base_model = create_transfer_model('/mnt/c/Users/nagas/deepfake-detection/video_cdf/saved_models_video/celebdf_models/final_resnet50_deepfake.h5')

# Compile with focal loss
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss=focal_loss(gamma=2., alpha=0.25),  # Use focal loss instead of binary crossentropy
    metrics=[
        'accuracy',
        tf.keras.metrics.AUC(name='auc'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall')
    ]
)

# Enhanced callbacks
callbacks_list = [
    callbacks.EarlyStopping(
        patience=8,
        restore_best_weights=True,
        monitor='val_auc',
        mode='max',
        verbose=1
    ),
    callbacks.ModelCheckpoint(
        'best_faceforensics_model.h5',
        save_best_only=True,
        monitor='val_auc',
        mode='max',
        verbose=1
    ),
    callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.3,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

# Progressive training approach
print("Phase 1: Training with frozen base model")
history1 = model.fit(
    train_gen,
    epochs=15,
    validation_data=val_gen,
    callbacks=callbacks_list,
    verbose=1
)

# Phase 2: Unfreeze some layers for fine-tuning
print("Phase 2: Fine-tuning with unfrozen layers")
for layer in base_model.layers[-30:]:  # Unfreeze last 30 layers
    layer.trainable = True

# Lower learning rate for fine-tuning
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # Lower LR
    loss=focal_loss(gamma=2., alpha=0.25),
    metrics=[
        'accuracy',
        tf.keras.metrics.AUC(name='auc'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall')
    ]
)

history2 = model.fit(
    train_gen,
    epochs=30,
    validation_data=val_gen,
    callbacks=callbacks_list,
    verbose=1
)

# Evaluate on test set
test_gen = val_test_datagen.flow_from_dataframe(
    dataframe=test_df,
    x_col='filepath',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=True
)

print("\nEvaluating on test set:")
test_metrics = model.evaluate(test_gen, verbose=1)
print(f"Test Results: Loss={test_metrics[0]:.4f}, Accuracy={test_metrics[1]:.4f}, AUC={test_metrics[2]:.4f}")

# Get predictions for detailed analysis
test_predictions = model.predict(test_gen)
test_predictions_binary = (test_predictions > 0.5).astype(int)

# Classification report
print("\nClassification Report:")
print(classification_report(test_gen.labels, test_predictions_binary.flatten()))

# Save the final model
model.save('final_faceforensics_resnet50.keras')
