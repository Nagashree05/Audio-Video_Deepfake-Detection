import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import tensorflow as tf

def plot_training_history(history, save_path=None):
    """Plot and optionally save training/validation metrics."""
    plt.figure(figsize=(18, 6))
    
    # Accuracy plot
    plt.subplot(1, 3, 1)
    plt.plot(history.history['accuracy'], label='Train', marker='o')
    plt.plot(history.history['val_accuracy'], label='Validation', marker='s')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Loss plot
    plt.subplot(1, 3, 2)
    plt.plot(history.history['loss'], label='Train', marker='o')
    plt.plot(history.history['val_loss'], label='Validation', marker='s')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    # AUC plot
    plt.subplot(1, 3, 3)
    if 'auc' in history.history:
        plt.plot(history.history['auc'], label='Train AUC', marker='o')
        plt.plot(history.history['val_auc'], label='Validation AUC', marker='s')
        plt.title('Model AUC')
        plt.xlabel('Epoch')
        plt.ylabel('AUC')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_confusion_matrix(y_true, y_pred, classes=['Real', 'Fake'], save_path=None):
    """Plot confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def print_classification_report(y_true, y_pred, target_names=['Real', 'Fake']):
    """Print detailed classification report."""
    print("\nClassification Report:")
    print("="*50)
    print(classification_report(y_true, y_pred, target_names=target_names))

def evaluate_model_comprehensive(model, test_generator, save_plots=True, save_dir="./"):
    """Comprehensive model evaluation with multiple metrics."""
    
    # Get predictions
    test_predictions = model.predict(test_generator, verbose=1)
    test_predictions_binary = (test_predictions > 0.5).astype(int).flatten()
    
    # Get true labels
    y_true = test_generator.labels
    
    # Basic metrics
    test_metrics = model.evaluate(test_generator, verbose=1)
    print(f"\nTest Metrics:")
    print(f"Loss: {test_metrics[0]:.4f}")
    print(f"Accuracy: {test_metrics[1]:.4f}")
    
    if len(test_metrics) > 2:
        print(f"AUC: {test_metrics[2]:.4f}")
        if len(test_metrics) > 3:
            print(f"Precision: {test_metrics[3]:.4f}")
            print(f"Recall: {test_metrics[4]:.4f}")
    
    # Classification report
    print_classification_report(y_true, test_predictions_binary)
    
    # Confusion matrix
    if save_plots:
        plot_confusion_matrix(y_true, test_predictions_binary, 
                            save_path=f"{save_dir}/confusion_matrix.png")
    
    # ROC Curve
    if save_plots:
        plot_roc_curve(y_true, test_predictions.flatten(), 
                      save_path=f"{save_dir}/roc_curve.png")
    
    return {
        'test_metrics': test_metrics,
        'predictions': test_predictions,
        'predictions_binary': test_predictions_binary,
        'true_labels': y_true
    }

def plot_roc_curve(y_true, y_pred_proba, save_path=None):
    """Plot ROC curve."""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def compare_models(model_results_dict, metric='accuracy'):
    """Compare multiple models performance."""
    models = list(model_results_dict.keys())
    scores = [model_results_dict[model][metric] for model in models]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(models, scores, color=['skyblue', 'lightgreen', 'lightcoral'])
    plt.title(f'Model Comparison - {metric.capitalize()}')
    plt.ylabel(metric.capitalize())
    plt.ylim([0, 1])
    
    # Add value labels on bars
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{score:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
