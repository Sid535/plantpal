import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import os

from model_config import (
    BATCH_SIZE, IMAGE_SIZE, SEED, VALIDATION_SPLIT, 
    training_model_list, training_model_name
)

# Keep the terminal clean
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

dataset_path = "data/plantvillage_dataset/color"

print(f"--- Evaluating {training_model_name} ---")

# 1. Recreate the EXACT test pool
# IMPORTANT: shuffle=False is required here so the labels don't mix up during prediction
val_test_pool = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names=training_model_list,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False 
)

# Skip the validation half to get the test half
val_batches = tf.data.experimental.cardinality(val_test_pool)
test_ds = val_test_pool.skip(val_batches // 2)

# 2. Load the saved model
model_path = f"server/models/{training_model_name}.keras"
if not os.path.exists(model_path):
    print(f"Error: Model not found at {model_path}. Train the model first.")
    exit()

print(f"Loading model from {model_path}...")
model = tf.keras.models.load_model(model_path)

# 3. Generate Predictions
print("Scanning test images and generating predictions. This may take a minute...")
true_labels = []
predictions = []

for images, labels in test_ds:
    true_labels.extend(labels.numpy())
    preds = model.predict(images, verbose=0)
    predictions.extend(np.argmax(preds, axis=1))

# 4. Print Classification Report (Precision, Recall, F1-Score)
print("\n" + "="*60)
print("             CLASSIFICATION REPORT")
print("="*60)
# Clean up class names for the terminal printout (removes "Tomato___")
clean_names = [name.split("___")[-1] for name in training_model_list]
print(classification_report(true_labels, predictions, target_names=clean_names))

# 5. Generate and Save the Confusion Matrix
print("\nGenerating Confusion Matrix...")
cm = confusion_matrix(true_labels, predictions)

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=clean_names, 
            yticklabels=clean_names)

plt.title(f'Confusion Matrix: {training_model_name}', fontsize=16)
plt.ylabel('Actual Real-World Disease', fontsize=12)
plt.xlabel('What the Model Predicted', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the plot as a PNG image
plot_path = f"server/models/{training_model_name}_confusion_matrix.png"
plt.savefig(plot_path, dpi=300)

print(f"SUCCESS! Confusion matrix saved to: {plot_path}")
print("="*60)