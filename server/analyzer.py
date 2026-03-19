import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'      # Hides standard TF warnings
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"     # FORCES TensorFlow to ignore GPUs completely

import tensorflow as tf
import numpy as np
from PIL import Image
from functools import lru_cache

from server.model_config import IMAGE_SIZE, PLANT_CONFIG, MODEL_PATHS
from server.treatments import TREATMENT_MAP

PLANT_MODELS = {
    plant.capitalize(): {
        "path": MODEL_PATHS[plant],
        "classes": PLANT_CONFIG[plant]["classes"]
    }
    for plant in PLANT_CONFIG
}

@lru_cache(maxsize=3)
def load_model(path):
    print(f"\n--- Loading {path} from Hard Drive into RAM ---")
    return tf.keras.models.load_model(path)

def analyze_plant_image(image_file, plant_type):
    if image_file is not None and plant_type in PLANT_MODELS:
        model_info = PLANT_MODELS[plant_type]
        
        model = load_model(model_info["path"])
        
        # Preprocess
        img = Image.open(image_file).convert('RGB')
        img = img.resize(IMAGE_SIZE)
        img_array = np.array(img).astype(np.float32)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array, verbose=0)
        result_index = np.argmax(predictions[0])
        full_label = model_info["classes"][result_index]

        # Formatting result (e.g. "Tomato___Late_blight" -> "Late blight")
        parts = full_label.split("___")
        condition = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
        confidence = float(np.max(predictions[0])) * 100
        
        treatment = TREATMENT_MAP.get(condition, TREATMENT_MAP["Unknown"])

        return {
            "plant_name": plant_type,
            "condition": condition,
            "confidence": confidence,
            "treatment": treatment
        }
    return None