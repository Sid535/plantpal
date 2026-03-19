# Detailed treatment database
TOMATO_TREATMENTS = {
    "Bacterial spot": "Remove infected plants; avoid overhead watering.",
    "Early blight": "Use pathogen-free seeds and rotate crops annually.",
    "Late blight": "Apply fungicides; remove and destroy infected plant debris.",
    "Leaf Mold": "Increase ventilation and reduce humidity around plants.",
    "Septoria leaf spot": "Remove lower infected leaves and apply organic fungicides.",
    "Spider mites Two-spotted spider mite": "Use neem oil or insecticidal soap; increase humidity.",
    "Target Spot": "Improve air circulation and keep foliage dry.",
    "Tomato Yellow Leaf Curl Virus": "Control whiteflies and remove infected plants.",
    "Tomato mosaic virus": "Remove infected plants; sanitize tools after use."
}

APPLE_TREATMENTS = {
    "Apple scab": "Rake fallen leaves and prune for better air circulation.",
    "Black rot": "Prune dead branches and remove mummified fruit.",
    "Cedar apple rust": "Remove nearby junipers and apply preventative fungicides."
}

CORN_TREATMENTS = {
    "Cercospora leaf spot Gray leaf spot": "Rotate crops and manage irrigation to reduce leaf wetness.",
    "Common rust": "Plant resistant hybrids; fungicides are rarely needed.",
    "Northern Leaf Blight": "Use resistant varieties and practice crop rotation."
}

GENERAL_TREATMENTS = {
    "healthy": "Your plant looks great! Maintain regular watering and care.",
    "Unknown": "Consult an agronomist for specific treatment advice."
}

TREATMENT_MAP = {**TOMATO_TREATMENTS, **APPLE_TREATMENTS, **CORN_TREATMENTS, **GENERAL_TREATMENTS}