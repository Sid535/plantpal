import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'      # Hides standard TF warnings
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"     # FORCES TensorFlow to ignore GPUs completely

import tensorflow as tf
import numpy as np
from PIL import Image
from functools import lru_cache

from server.model_config import IMAGE_SIZE, ALL_CLASSES, MODEL_PATHS
from server.treatments import PLANT_INFO
from server.translations import get_translated_info

MODEL_PATH = MODEL_PATHS["plantpal"]

@lru_cache(maxsize=1)
def load_model(path):
    print(f"\n--- Loading {path} from Hard Drive into RAM ---")
    return tf.keras.models.load_model(path)

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
    img = img.resize(IMAGE_SIZE)
    img_array = np.array(img).astype(np.float32)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)
    result_index = np.argmax(predictions[0])
    full_label = ALL_CLASSES[result_index]
    
    parts = full_label.split("___")
    plant_name = parts[0].split("_(")[0]
    condition = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown"
    confidence = float(np.max(predictions[0])) * 100
    
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
        "info": translated_info,  # Now contains translated disease info
        "language": language  # Include language in response for verification
    }
