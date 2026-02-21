import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
import os
from config import BATCH_SIZE, IMAGE_SIZE, tomato_classes

dataset_path = "data/plantvillage_dataset/"

# Load Dataset with Memory Optimizations
train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names = tomato_classes,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names = tomato_classes,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

# Optimization: Prefetching overlaps data preprocessing and model execution
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Build Model (Transfer Learning)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False 

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(len(train_ds.class_names), activation='softmax')
])

# Compile and Train
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Start with fewer epochs to test stability
model.fit(train_ds, validation_data=val_ds, epochs=5)

# Save the Model
if not os.path.exists('server'):
    os.makedirs('server')
model.save("server/tomato_model.h5")