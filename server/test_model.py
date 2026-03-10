import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
import os
from model_config import IMAGE_SIZE, training_model_list

# Model Path
model_path = "server/models/tomato_model.keras"
#directory containing your test images
test_dir_path = "server/test_data/tomato/"

if not os.path.exists(test_dir_path):
    print(f"Error: Directory not found at {test_dir_path}")
else:
    # Load the model once
    print("Loading Fine-Tuned Model...")
    model = tf.keras.models.load_model(model_path)
    
    # Get list of all image files in the directory
    image_files = [f for f in os.listdir(test_dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print(f"No images found in {test_dir_path}")
    else:
        print(f"Found {len(image_files)} images. Starting batch analysis...\n")
        
        # Track statistics for professional benchmarking
        correct_count = 0
        total_confidence = 0

        # 3. Loop through every image in the directory
        for img_name in image_files:
            img_path = os.path.join(test_dir_path, img_name)
            
            # Preprocess the image
            img = image.load_img(img_path, target_size=IMAGE_SIZE)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)

            # 4. Predict
            predictions = model.predict(img_array, verbose=0)
            
            # 5. Output Result
            class_idx = np.argmax(predictions[0])
            confidence = 100 * np.max(predictions[0])
            result_label = training_model_list[class_idx]
            
            total_confidence += confidence

            print(f"File: {img_name}")
            print(f"Prediction: {result_label} ({confidence:.2f}%)")
            
            if confidence < 70:
                print("--> WARNING: Low confidence result.")
            print("-" * 20)

        # 6. Final Benchmark Summary
        avg_confidence = total_confidence / len(image_files)
        print("\n" + "="*30)
        print("BATCH TEST SUMMARY")
        print(f"Total Images Tested: {len(image_files)}")
        print(f"Average Confidence: {avg_confidence:.2f}%")
        print("="*30)
