import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
from tensorflow.keras.applications import MobileNetV2 # type: ignore
import os
from model_config import BATCH_SIZE, IMAGE_SIZE, training_model_list, training_model_name

# --- SAFETY: Prevent System Lockup ---
# Limits TensorFlow to only use 2 CPU cores so OS stays responsive
tf.config.threading.set_intra_op_parallelism_threads(3)
tf.config.threading.set_inter_op_parallelism_threads(3)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# use data/plantvillage_dataset/greyscale or data/plantvillage_dataset/segmented for diffrent
dataset_path = "data/plantvillage_dataset/color"

# Load Dataset with Memory Optimizations
raw_train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names = training_model_list,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

raw_val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names = training_model_list,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

num_classes = len(raw_train_ds.class_names)
AUTOTUNE = tf.data.AUTOTUNE

# --- OPTIMIZATION: Memory-Safe Pipeline ---
# REMOVED: .cache() - This was likely filling your RAM and crashing the PC.
# REDUCED: shuffle(500) - Lower buffer size saves memory.
train_ds = raw_train_ds.shuffle(500).prefetch(buffer_size=AUTOTUNE)
val_ds = raw_val_ds.prefetch(buffer_size=AUTOTUNE)

# Build Model (Transfer Learning)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# STEP 1: FREEZE BASE MODEL (Warming up the head)
base_model.trainable = False

model = models.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.Rescaling(1./127.5, offset=-1),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])


# COMPILE & TRAIN PHASE 1
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("Phase 1: Training the Head...")
model.fit(train_ds, validation_data=val_ds, epochs=3)

# STEP 2: UNFREEZE FOR FINE-TUNING
print("Phase 2: Fine-Tuning...")
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Compile with a lower Learning Rate for fine-tuning
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy']
)

# Set up Early Stopping
# Stop if validation loss doesn't improve for 2 epochs and restore the best weights
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', 
    patience=3, 
    restore_best_weights=True
)

# Train
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    callbacks=[early_stop]
)

# Save the Model
model.save(f"server/models/{training_model_name}.keras")
print(f"Successfully saved: server/models/{training_model_name}.keras")