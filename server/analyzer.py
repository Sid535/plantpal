# server/analyzer.py

def analyze_plant_image(image_file):
    if image_file is not None:
        # Mock results for demonstration
        result = {
            "plant_name": "Tomato",
            "condition": "Late Blight",
            "treatment": "Remove infected leaves and apply a copper-based fungicide."
        }
        return result
    return None