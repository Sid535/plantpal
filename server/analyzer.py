import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'      # Hides standard TF warnings
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"     # FORCES TensorFlow to ignore GPUs completely

import tensorflow as tf
import numpy as np
from PIL import Image
from functools import lru_cache
import base64
import cv2

from server.model_config import IMAGE_SIZE, ALL_CLASSES, MODEL_PATHS
from server.treatments import PLANT_INFO
from server.translations import get_translated_info

MODEL_PATH = MODEL_PATHS["plantpal"]

@lru_cache(maxsize=1)
def load_model(path):
    print(f"\n--- Loading {path} from Hard Drive into RAM ---")
    return tf.keras.models.load_model(path)

def get_img_array(img):
    img = img.resize(IMAGE_SIZE)
    img_array = np.array(img).astype(np.float32)
    return np.expand_dims(img_array, axis=0)

def make_gradcam_heatmap(img_array, model, pred_index=None):
    """
    Generates a Grad-CAM heatmap for the given image.
    
    How it works:
    1. Computes how much each feature map channel contributed to the final prediction
    2. Uses gradients to weight the importance of each feature map
    3. Creates a 2D heatmap showing the important regions
    """
    # Convert to tensor
    img_tensor = tf.cast(img_array, tf.float32)
    
    # Get the mobilenetv2 layer
    mobilenetv2_layer = model.get_layer('mobilenetv2_1.00_224')
    
    # Use GradientTape to record operations
    with tf.GradientTape() as tape:
        # Forward pass to get conv outputs and predictions
        conv_outputs = mobilenetv2_layer(img_tensor, training=False)
        tape.watch(conv_outputs)
        
        # Continue through remaining layers after mobilenetv2
        x = conv_outputs
        for layer in model.layers[model.layers.index(mobilenetv2_layer) + 1:]:
            x = layer(x, training=False)
        
        predictions = x
        
        # Get the predicted class index
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        
        # Get the score for the predicted class
        class_score = predictions[:, pred_index]
    
    # Compute gradient of class score w.r.t. conv layer output
    grads = tape.gradient(class_score, conv_outputs)
    
    # Handle None gradients (fallback)
    if grads is None:
        heatmap = tf.reduce_mean(tf.abs(conv_outputs), axis=-1)[0]
    else:
        # Average the gradients across spatial dimensions
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Weight each feature map channel by its gradient
        conv_outputs_single = conv_outputs[0]
        heatmap = conv_outputs_single @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
    
    # Apply ReLU and normalize
    heatmap = tf.maximum(heatmap, 0)
    heatmap_max = tf.math.reduce_max(heatmap)
    if heatmap_max > 1e-8:
        heatmap = heatmap / heatmap_max
    
    return heatmap.numpy()

def get_gradcam_image(img, heatmap):
    # We use cv2 to superimpose the heatmap on original image
    img = np.array(img)
    
    # Resize heatmap to match input image size
    heatmap_resized = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Invert: the heatmap values are importance scores where high = important
    # But we want the jet colormap to show red for important areas
    # In jet colormap: blue (0) = cold, red (255) = hot
    # So we invert so that high importance becomes high values (red)
    heatmap_resized = 1.0 - heatmap_resized  # Invert the values
    heatmap_resized = np.uint8(255 * heatmap_resized)

    # Use jet colormap to colorize heatmap
    # After inversion: important areas (high values) → RED
    jet = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)

    # Use RGB values of the colormap
    jet_colors = jet[..., ::-1]

    # Superimpose the heatmap on original image with 40% opacity
    superimposed_img = jet_colors * 0.4 + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    
    # Encode to base64
    _, buffer = cv2.imencode('.jpg', superimposed_img)
    return base64.b64encode(buffer).decode('utf-8')


def analyze_plant_image(image_file, language: str = "en"):
    if image_file is None:
        return None
    
    # Validate language
    valid_langs = ["en", "hi", "mr"]
    if language not in valid_langs:
        language = "en"
        
    model = load_model(MODEL_PATH)
        
    # Preprocess
    img = Image.open(image_file).convert('RGB')
    img_array = get_img_array(img)

    predictions = model.predict(img_array, verbose=0)
    result_index = np.argmax(predictions[0])
    full_label = ALL_CLASSES[result_index]
    
    parts = full_label.split("___")
    plant_name = parts[0].split("_(")[0]
    condition = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown"
    confidence = float(np.max(predictions[0])) * 100
    
    # Grad-CAM
    heatmap = make_gradcam_heatmap(img_array, model)
    gradcam_image = get_gradcam_image(img.resize(IMAGE_SIZE), heatmap)
    
    # Get translated info based on language
    translated_info = get_translated_info(full_label, language)
    
    # Fallback to English PLANT_INFO if translation not available
    if not translated_info:
        translated_info = PLANT_INFO.get(full_label, {})

    return {
        "plant_name": plant_name,
        "condition": condition,
        "confidence": confidence,
        "low_confidence": confidence < 70,
        "info": translated_info,
        "gradcam_image": gradcam_image,
        "language": language
    }
