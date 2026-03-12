from PIL import Image
from pathlib import Path
import sys

def clean_corrupted_images(path):
    dataset_path = Path(path)
    if not dataset_path.exists():
        print(f"Error: The path {path} does not exist.")
        return

    # Find all images first to know the total count
    print(f"Scanning for images in {path}...")
    img_list = [p for p in dataset_path.rglob("*") if p.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    total = len(img_list)
    
    print(f"Starting cleanup of {total} images...")
    corrupted_count = 0

    for i, img_path in enumerate(img_list):
        try:
            # We open and verify the image
            with Image.open(img_path) as img:
                img.verify()
        except (IOError, SyntaxError):
            print(f"\n[X] Deleting corrupted: {img_path}")
            img_path.unlink()
            corrupted_count += 1
        
        # Simple progress indicator for your terminal
        if i % 100 == 0 or i == total - 1:
            percent = (i + 1) / total * 100
            sys.stdout.write(f"\rProgress: [{i+1}/{total}] {percent:.1f}% complete")
            sys.stdout.flush()

    print(f"\n\nCleanup finished!")
    print(f"Total checked: {total}")
    print(f"Corrupted files removed: {corrupted_count}")

if __name__ == "__main__":
    clean_corrupted_images("data/plantvillage_dataset/color")