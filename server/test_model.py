import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
from model_config import IMAGE_SIZE, training_model_list

# 1. Path setup
model_path = "server/models/tomato_model.keras"
# Update this to the actual image you want to test
test_image_path = "test_data/tomato/early_blight_test.jpg" 

if not os.path.exists(test_image_path):
    print(f"Error: File not found at {test_image_path}")
else:
    # 2. Load the model (Keras format handles architecture + weights)
    print("Loading Fine-Tuned Model...")
    model = tf.keras.models.load_model(model_path)

    # 3. Preprocess the image
    img = image.load_img(test_image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Note: Our model has a layers.Rescaling(1./127.5, offset=-1) built-in,
    # so we don't need to manually divide by 255 here.

    # 4. Predict
    print("Analyzing image...")
    predictions = model.predict(img_array)
    
    # 5. Output Result
    class_idx = np.argmax(predictions[0])
    confidence = 100 * np.max(predictions[0])
    
    # Get the predicted label
    result_label = training_model_list[class_idx]

    print("\n" + "="*30)
    print(f"RESULT: {result_label}")
    print(f"CONFIDENCE: {confidence:.2f}%")
    print("="*30)

    # Troubleshooting check
    if confidence < 70:
        print("\nNote: Low confidence. The model might need more diverse training data")
        print("or the image might have lighting/angle issues.")