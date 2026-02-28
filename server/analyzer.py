import tensorflow as tf
import numpy as np
from PIL import Image
from server.model_config import apple_class, corn_class, tomato_classes, IMAGE_SIZE

PLANT_MODELS = {
    "Apple": {"path": "server/models/apple_model.keras", "classes": apple_class},
    "Corn": {"path": "server/models/corn_model.keras", "classes": corn_class},
    "Tomato": {"path": "server/models/tomato_model.keras", "classes": tomato_classes}
}

def analyze_plant_image(image_file, plant_type):
    if image_file is not None and plant_type in PLANT_MODELS:
        model_info = PLANT_MODELS[plant_type]
        # Load the selected model
        model = tf.keras.models.load_model(model_info["path"])
        
        # Preprocess
        img = Image.open(image_file).convert('RGB')
        img = img.resize(IMAGE_SIZE)
        img_array = np.array(img).astype(np.float32) # Convert to float
        img_array = np.expand_dims(img_array, axis=0) # Add batch dimension

        predictions = model.predict(img_array)
        result_index = np.argmax(predictions[0])
        full_label = model_info["classes"][result_index]

        # Formatting result (e.g. "Tomato___Late_blight" -> "Late blight")
        parts = full_label.split("___")
        condition = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"

        return {
            "plant_name": plant_type,
            "condition": condition,
            "treatment": "Follow standard organic or chemical treatment based on local guidelines."
        }
    return None