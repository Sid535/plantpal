import sys
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from server.model_config import (
    BATCH_SIZE, IMAGE_SIZE, SEED, VALIDATION_SPLIT, 
    ALL_CLASSES, MODEL_PATHS
)

def evaluate():
    training_model_list = ALL_CLASSES
    model_path = MODEL_PATHS["plantpal"]
    model_name = "plantpal_model"
    
    ROOT = Path(__file__).resolve().parent.parent
    dataset_path = str(ROOT / "data" / "plantvillage_dataset" / "color")

    print(f"--- Evaluating {model_name} ---")
    
    test_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        class_names=training_model_list,
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}. Train the model first.")
        sys.exit(1)

    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)

    # 3. Generate Predictions
    print("Scanning test images and generating predictions. This may take a minute...")
    true_labels, predictions = [], []

    for images, labels in test_ds:
        true_labels.extend(labels.numpy())
        preds = model.predict(images, verbose=0)
        predictions.extend(np.argmax(preds, axis=1))

    clean_names = [name.split("___")[-1] for name in training_model_list]
    
    # 4. Print Classification Report (Precision, Recall, F1-Score)
    print("\n" + "="*60)
    print("             CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(true_labels, predictions, target_names=clean_names))

    # 5. Generate and Save the Confusion Matrix
    print("\nGenerating Confusion Matrix...")
    cm = confusion_matrix(true_labels, predictions)

    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=clean_names, 
                yticklabels=clean_names)

    plt.title(f'Confusion Matrix: {model_name}', fontsize=16)
    plt.ylabel('Actual Real-World Disease', fontsize=12)
    plt.xlabel('What the Model Predicted', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as a PNG image
    plot_path = str(ROOT / "server" / "reports" / "confusion_matrix" / f"{model_name}_confusion_matrix.png")
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path, dpi=300)

    print(f"Confusion matrix saved to: {plot_path}")
    print("="*60)

if __name__ == "__main__":
    evaluate()