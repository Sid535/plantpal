import os
import random
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dataset_path = str(ROOT / "data" / "plantvillage_dataset" / "color")

def clean_dataset():
    print("=== Phase 1: Scanning for Corrupted Images ===")
    corrupted_files = []
    total_checked = 0

    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path '{dataset_path}' not found.")
        return

    for class_name in os.listdir(dataset_path):
        class_folder = os.path.join(dataset_path, class_name)
        if not os.path.isdir(class_folder):
            continue

        for img_file in os.listdir(class_folder):
            img_path = os.path.join(class_folder, img_file)
            total_checked += 1

            try:
                # verify() checks the file headers without loading the full image into RAM
                img = Image.open(img_path)
                img.verify()   
            except Exception:
                corrupted_files.append(img_path)

    print(f"Scan complete! Checked {total_checked} images.")
    
    if corrupted_files:
        print(f"Found {len(corrupted_files)} corrupted files. Deleting now...")
        for bad_file in corrupted_files:
            os.remove(bad_file)
            print(f"  -> Deleted: {bad_file}")
        print("Dataset is now 100% clean.")
    else:
        print("No corrupted files found. Dataset is perfectly clean!")

def visualize_distribution():
    print("\n=== Phase 2: Generating Class Distribution Chart ===")
    class_counts = {}
    
    for class_name in os.listdir(dataset_path):
        class_folder = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_folder):
            # Clean up the name for the chart (Removes "Tomato___")
            clean_name = class_name.split("___")[-1].replace("_", " ")
            class_counts[clean_name] = len(os.listdir(class_folder))

    df = pd.DataFrame(list(class_counts.items()), columns=['Disease', 'Image Count'])
    df = df.sort_values('Image Count', ascending=False)

    plt.figure(figsize=(14, 8))
    bars = plt.bar(df['Disease'], df['Image Count'], color='steelblue')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.title('PlantVillage Dataset: Image Distribution per Disease', fontsize=16)
    plt.ylabel('Number of Images', fontsize=12)
    plt.xlabel('Disease Class', fontsize=12)
    plt.tight_layout()

    # Add the exact numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha='center', va='bottom', fontsize=9)

    save_path = str(ROOT / "server" / "reports" / "dataset_distribution.png")
    plt.savefig(save_path, dpi=300)
    print(f"Chart saved successfully to: {save_path}")

def generate_sample_grid():
    print("\n=== Phase 3: Generating Random Sample Grid ===")
    classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    
    # Pick 9 random classes to display in a 3x3 grid
    sampled_classes = random.sample(classes, min(9, len(classes)))
    fig, axes = plt.subplots(3, 3, figsize=(10, 10))

    for ax, cls in zip(axes.flatten(), sampled_classes):
        class_folder = os.path.join(dataset_path, cls)
        random_image = random.choice(os.listdir(class_folder))
        img_path = os.path.join(class_folder, random_image)

        img = Image.open(img_path)
        ax.imshow(img)

        clean_name = cls.split("___")[-1].replace("_", " ")
        ax.set_title(clean_name, fontsize=10, pad=6)
        ax.axis('off')

    plt.suptitle('Random Samples from the Dataset', fontsize=16)
    plt.tight_layout()
    
    save_path = str(ROOT / "server" / "reports" / "dataset_samples.png")
    plt.savefig(save_path, dpi=300)
    print(f"Sample grid saved successfully to: {save_path}")

if __name__ == "__main__":
    clean_dataset()
    visualize_distribution()
    generate_sample_grid()
    print("\nAll dataset tools executed successfully!")