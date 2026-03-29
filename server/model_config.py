# --- HARDWARE & SYSTEM CONFIG ---
BATCH_SIZE = 32 # 32 for colab, 8 for local
CPU_THREADS = 8 # 8 for colob, 3 for local
SHUFFLE_BUFFER = 500
SEED = 123

# --- IMAGE & DATASET CONFIG ---
IMAGE_SIZE = (224, 224)
IMAGE_CHANNELS = 3
VALIDATION_SPLIT = 0.2 
ROTATION_FACTOR = 0.2
DROPOUT_RATE = 0.3

# --- TRAINING HYPERPARAMETERS ---
PHASE_1_EPOCHS = 3
PHASE_2_EPOCHS = 30
FINE_TUNE_LAYERS = 20
FINE_TUNE_LR = 1e-5
EARLY_STOP_PATIENCE = 3
BRIGHTNESS_FACTOR = 0.2
CONTRAST_FACTOR = 0.2

apple_class = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
]

blueberry_class = [
    'Blueberry___healthy',
]

cherry_class = [
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
]

corn_class = [
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
]

grape_class = [
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
]

orange_class = [
    'Orange___Haunglongbing_(Citrus_greening)',
]

peach_class = [
    'Peach___Bacterial_spot',
    'Peach___healthy',
]

pepper_bell_class = [
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
]

potato_class = [
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
]

raspberry_class = [
    'Raspberry___healthy',
]

soybean_class = [
    'Soybean___healthy',
]

squash_class = [
    'Squash___Powdery_mildew',
]

strawberry_class = [
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
]

tomato_class = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
]

ALL_CLASSES = [
    *apple_class,
    *blueberry_class,
    *cherry_class,
    *corn_class,
    *grape_class,
    *orange_class,
    *peach_class,
    *pepper_bell_class,
    *potato_class,
    *raspberry_class,
    *soybean_class,
    *squash_class,
    *strawberry_class,
    *tomato_class,
]

PLANT_CONFIG = {
    "apple": {"classes": apple_class},
    "corn":  {"classes": corn_class},
    "tomato": {"classes": tomato_class},
}

MODEL_PATHS = {
    "plantpal": "server/models/plantpal_model.keras",
    "custom_cnn": "server/models/custom_cnn.keras",
    "vgg16_model": "server/models/vgg16_model.keras"
}