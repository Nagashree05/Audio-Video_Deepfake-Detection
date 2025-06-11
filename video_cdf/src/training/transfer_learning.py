import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras import layers, Input
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def load_pretrained_model(model_path):
    """Load model with error handling"""
    try:
        model = load_model(model_path)
        print(f"Loaded pretrained model from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def create_transfer_model(pretrained_model_path, num_classes=1):
    """Create transfer learning model with proper input handling"""
    # Load base model
    base_model = load_pretrained_model(pretrained_model_path)
    
    if base_model is None:
        print("Using ImageNet-pretrained ResNet50")
        base_model = tf.keras.applications.ResNet50(
            weights='imagenet', 
            include_top=False, 
            input_shape=(224, 224, 3)
        )
        last_conv = base_model.get_layer('conv5_block3_out')  # Standard ResNet50 last conv layer
    else:
        # Find last valid convolutional layer with 4D output
        last_conv = None
        for layer in reversed(base_model.layers):
            if hasattr(layer, 'output') and len(layer.output.shape) == 4:
                last_conv = layer
                break
        
        if not last_conv:
            raise ValueError("No 4D convolutional layer found in the base model")

    # Create explicit input tensor
    inputs = Input(shape=(224, 224, 3), name='new_input')
    
    # Rebuild feature extractor using Functional API
    if base_model is None:
        x = base_model(inputs)
    else:
        # Handle Sequential models by recreating the architecture
        x = inputs
        for layer in base_model.layers:
            x = layer(x)
            if layer == last_conv:
                break

    # Build new head
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation='sigmoid')(x)

    # Create final model
    model = Model(inputs=inputs, outputs=outputs)
    
    # Freeze convolutional base
    for layer in model.layers[:-5]:  # Freeze all layers except last 5
        layer.trainable = False

    # Compile with focal loss
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss=tf.keras.losses.BinaryFocalCrossentropy(gamma=2.0, alpha=0.25),
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    
    return model

if __name__ == "__main__":
    model = create_transfer_model("/mnt/c/Users/nagas/deepfake-detection/video_cdf/saved_models_video/celebdf_models/final_resnet50_deepfake.h5")
    model.summary()
