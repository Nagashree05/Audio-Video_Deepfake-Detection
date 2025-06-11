import os
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import (accuracy_score, classification_report, 
                             confusion_matrix, roc_auc_score, RocCurveDisplay)

# Configuration
PROCESSED_DIR = 'processed_audio_data'
MODEL_DIR = 'saved_models'
PLOT_DIR = 'evaluation_plots'
os.makedirs(PLOT_DIR, exist_ok=True)

# Load data and model
X_test = np.load(os.path.join(PROCESSED_DIR, 'X_test.npy'))
y_test = np.load(os.path.join(PROCESSED_DIR, 'y_test.npy'))
X_test = np.expand_dims(X_test, -1)
model = tf.keras.models.load_model(os.path.join(MODEL_DIR, 'best_model.keras'))

# Convert labels
y_test = tf.keras.utils.to_categorical(y_test)
y_true = np.argmax(y_test, axis=1)

# Generate predictions
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Calculate metrics
accuracy = accuracy_score(y_true, y_pred_classes)
auc = roc_auc_score(y_true, y_pred[:, 1])
report = classification_report(y_true, y_pred_classes)
cm = confusion_matrix(y_true, y_pred_classes)

# Save metrics
with open(os.path.join(PLOT_DIR, 'metrics.txt'), 'w') as f:
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"AUC-ROC: {auc:.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)

# Plot ROC curve
plt.figure(figsize=(8, 6))
RocCurveDisplay.from_predictions(y_true, y_pred[:, 1])
plt.title('ROC Curve')
plt.savefig(os.path.join(PLOT_DIR, 'roc_curve.png'))
plt.close()

# Plot confusion matrix
plt.figure(figsize=(6, 6))
plt.imshow(cm, cmap='Blues')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted')
plt.ylabel('True')
plt.xticks([0, 1], ['Real', 'Fake'])
plt.yticks([0, 1], ['Real', 'Fake'])
for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i, j]), ha='center', va='center')
plt.savefig(os.path.join(PLOT_DIR, 'confusion_matrix.png'))
plt.close()

print("Evaluation complete! Results saved in:", PLOT_DIR)
