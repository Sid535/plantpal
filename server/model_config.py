BATCH_SIZE = 8
IMAGE_SIZE = (224, 224)

# --- HARDWARE & SYSTEM CONFIG ---
BATCH_SIZE = 8
CPU_THREADS = 3         # Limits TensorFlow threads to prevent OS lockups
SHUFFLE_BUFFER = 500    # Keeps RAM usage low during dataset shuffling
SEED = 123              # Ensures reproducibility across different training runs

# --- IMAGE & DATASET CONFIG ---
IMAGE_SIZE = (224, 224)
IMAGE_CHANNELS = 3
VALIDATION_SPLIT = 0.2  # Reserves 20% of data for the val/test pool
ROTATION_FACTOR = 0.2   # Range for random image rotation during augmentation
DROPOUT_RATE = 0.3      # Drops 30% of connections to prevent overfitting

# --- TRAINING HYPERPARAMETERS ---
PHASE_1_EPOCHS = 3
PHASE_2_EPOCHS = 30
FINE_TUNE_LAYERS = 20   # Number of base model layers to unfreeze
FINE_TUNE_LR = 1e-5     # Low learning rate prevents destroying pre-trained weights
EARLY_STOP_PATIENCE = 3 # Halts training if val_loss stops improving
BRIGHTNESS_FACTOR = 0.2
CONTRAST_FACTOR = 0.2

master_classes = [
    'Apple___healthy',
    'Tomato___healthy',
]

tomato_class = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___healthy',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
]

apple_class = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy'
]

corn_class = [
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___healthy",
    "Corn_(maize)___Northern_Leaf_Blight"
]

potato_class = []

training_model_list = tomato_class
training_model_name = "tomato_model_v2"