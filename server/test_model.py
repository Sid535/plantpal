import tensorflow as tf
import numpy as np
import argparse
import sys
import os
from PIL import Image
from pathlib import Path

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from server.model_config import IMAGE_SIZE, PLANT_CONFIG, MODEL_PATHS

def test(plant: str):
    config = PLANT_CONFIG[plant]
    training_model_list = config["classes"]
    model_path = MODEL_PATHS[plant]
    
    ROOT = Path(__file__).resolve().parent.parent
    test_dir_path = str(ROOT / "server" / "test_data" / plant)

    if not os.path.exists(test_dir_path):
        print(f"Error: Directory not found at {test_dir_path}")
        sys.exit(1)
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
        
    # Get list of all image files in the directory
    image_files = [f for f in os.listdir(test_dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"No images found in {test_dir_path}")
        sys.exit(1)
    
    print(f"Found {len(image_files)} images. Starting batch analysis...\n")
            
    # Track statistics for professional benchmarking
    total_confidence = 0

    # 3. Loop through every image in the directory
    for img_name in image_files:
        img_path = os.path.join(test_dir_path, img_name)
                
        # Preprocess the image
        img = Image.open(img_path).convert('RGB')
        img = img.resize(IMAGE_SIZE)
        img_array = np.array(img).astype(np.float32)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array, verbose=0)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch test a PlantPal model")
    parser.add_argument(
        "--plant",
        required=True,
        choices=PLANT_CONFIG.keys(),
        help="Which plant model to test"
    )
    args = parser.parse_args()
    test(args.plant)