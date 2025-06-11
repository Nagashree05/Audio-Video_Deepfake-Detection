import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.utils import class_weight

# Configuration
PROCESSED_DIR = 'processed_audio_data'
MODEL_DIR = 'saved_models'
os.makedirs(MODEL_DIR, exist_ok=True)

# Load processed data
X_train = np.load(os.path.join(PROCESSED_DIR, 'X_train.npy'))
X_val = np.load(os.path.join(PROCESSED_DIR, 'X_val.npy'))
X_test = np.load(os.path.join(PROCESSED_DIR, 'X_test.npy'))
y_train = np.load(os.path.join(PROCESSED_DIR, 'y_train.npy'))
y_val = np.load(os.path.join(PROCESSED_DIR, 'y_val.npy'))
y_test = np.load(os.path.join(PROCESSED_DIR, 'y_test.npy'))

# Add channel dimension
X_train = np.expand_dims(X_train, -1)
X_val = np.expand_dims(X_val, -1)
X_test = np.expand_dims(X_test, -1)

# Convert labels to categorical
y_train = tf.keras.utils.to_categorical(y_train)
y_val = tf.keras.utils.to_categorical(y_val)
y_test = tf.keras.utils.to_categorical(y_test)

def build_hybrid_model(input_shape):
    inputs = layers.Input(shape=input_shape)
    
    # CNN Branch
    x = layers.Conv2D(32, (3,3), activation='relu')(inputs)
    x = layers.MaxPooling2D((2,2))(x)
    x = layers.Conv2D(64, (3,3), activation='relu')(x)
    x = layers.MaxPooling2D((2,2))(x)
    x = layers.Flatten()(x)
    
    # LSTM Branch
    y = layers.Reshape((input_shape[0], input_shape[1], 1))(inputs)
    y = layers.TimeDistributed(layers.Conv1D(32, 3, activation='relu'))(y)
    y = layers.TimeDistributed(layers.MaxPooling1D(2))(y)
    y = layers.TimeDistributed(layers.Flatten())(y)
    y = layers.LSTM(128, return_sequences=True)(y)
    y = layers.LSTM(64)(y)
    
    # Combined
    combined = layers.concatenate([x, y])
    
    # Classifier
    z = layers.Dense(128, activation='relu')(combined)
    z = layers.Dropout(0.5)(z)
    outputs = layers.Dense(2, activation='softmax')(z)
    
    model = models.Model(inputs, outputs)
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    return model

# Class weights
class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(np.argmax(y_train, axis=1)), 
                                                  y=np.argmax(y_train, axis=1))
class_weights = {i: weight for i, weight in enumerate(class_weights)}

# Callbacks
early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
checkpoint = callbacks.ModelCheckpoint(
    os.path.join(MODEL_DIR, 'best_model.keras'),
    monitor='val_auc',
    mode='max',
    save_best_only=True
)
reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5)

# Build and train model
model = build_hybrid_model(X_train.shape[1:])
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=64,
    class_weight=class_weights,
    callbacks=[early_stop, checkpoint, reduce_lr]
)

# Save final model
model.save(os.path.join(MODEL_DIR, 'final_model.keras'))
