# src/models/resnet_models.py
import os
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models, Model
from tensorflow.keras.models import load_model

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def build_resnet50_model(input_shape=(224, 224, 3), num_classes=1):
    """Build standard ResNet50 model for deepfake detection."""
    base = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze first 140 layers for better feature preservation
    for layer in base.layers[:140]:
        layer.trainable = False
        
    # Use Functional API for better architecture control
    x = base.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation='sigmoid')(x)
    
    model = Model(inputs=base.input, outputs=outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    
    return model

def build_enhanced_model(input_shape=(224, 224, 3), num_classes=1):
    """Enhanced ResNet50 with regularization and deeper head."""
    base = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze first 160 layers
    for layer in base.layers[:160]:
        layer.trainable = False
    
    # Enhanced architecture with regularization
    x = base.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu',
                    kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)
    x = layers.Dropout(0.6)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation='sigmoid')(x)
    
    model = Model(inputs=base.input, outputs=outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss=tf.keras.losses.BinaryFocalCrossentropy(gamma=2.0, alpha=0.25),
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    
    return model

def create_transfer_model(pretrained_path, num_classes=1):
    """Create transfer learning model with proper dimension handling."""
    try:
        base_model = load_pretrained_model(pretrained_path)
        print(f"Loaded pretrained model from {pretrained_path}")
    except Exception as e:
        raise ValueError(f"Error loading model: {e}") from e

    # Find last 4D convolutional layer
    last_conv_layer = None
    for layer in reversed(base_model.layers):
        if len(layer.output.shape) == 4:
            last_conv_layer = layer
            break
    
    if not last_conv_layer:
        raise ValueError("No 4D convolutional layer found in base model")

    # Create feature extractor
    feature_extractor = Model(
        inputs=base_model.layers[0].input,
        outputs=last_conv_layer.output
    )

    # Freeze initial layers
    for layer in feature_extractor.layers[:140]:
        layer.trainable = False

    # Build new head
    inputs = layers.Input(shape=(224, 224, 3))
    x = feature_extractor(inputs)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.BatchNormalization()(x)
    outputs = layers.Dense(num_classes, activation='sigmoid')(x)

    # Create final model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile with focal loss
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss=tf.keras.losses.BinaryFocalCrossentropy(gamma=2.0, alpha=0.25),
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    
    return model, feature_extractor

def load_pretrained_model(model_path):
    """Safe model loader with error handling"""
    try:
        model = load_model(model_path)
        model._name = f"transfer_{model.name}"  # Avoid name conflicts
        return model
    except Exception as e:
        print(f"Error loading {model_path}: {str(e)}")
        return None
