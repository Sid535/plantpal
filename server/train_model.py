import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
from tensorflow.keras.applications import MobileNetV2 # type: ignore
import os

from model_config import (
    BATCH_SIZE, IMAGE_SIZE, IMAGE_CHANNELS, CPU_THREADS, 
    SHUFFLE_BUFFER, SEED, VALIDATION_SPLIT, ROTATION_FACTOR, 
    DROPOUT_RATE, PHASE_1_EPOCHS, PHASE_2_EPOCHS, FINE_TUNE_LAYERS, 
    FINE_TUNE_LR, EARLY_STOP_PATIENCE, BRIGHTNESS_FACTOR, CONTRAST_FACTOR, 
    training_model_list, training_model_name
)

tf.config.threading.set_intra_op_parallelism_threads(CPU_THREADS)
tf.config.threading.set_inter_op_parallelism_threads(CPU_THREADS)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

dataset_path = "data/plantvillage_dataset/color"

raw_train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names=training_model_list,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_test_pool = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    class_names = training_model_list,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_batches = val_test_pool.cardinality()
raw_val_ds = val_test_pool.take(val_batches // 2)
raw_test_ds = val_test_pool.skip(val_batches // 2)

num_classes = len(raw_train_ds.class_names)

class_counts = []
for class_name in training_model_list:
    class_dir = os.path.join(dataset_path, class_name)
    if os.path.exists(class_dir):
        count = len([f for f in os.listdir(class_dir) if os.path.isfile(os.path.join(class_dir, f))])
    else:
        count = 0
    class_counts.append(count)

total_images = sum(class_counts)
class_weights = {}

for i, count in enumerate(class_counts):
    if count > 0:
        weight = total_images / (num_classes * count)
        class_weights[i] = weight
    else:
        class_weights[i] = 1.0

print(f"\nComputed Class Weights: {class_weights}\n")

AUTOTUNE = tf.data.AUTOTUNE

train_ds = raw_train_ds.shuffle(SHUFFLE_BUFFER).prefetch(buffer_size=AUTOTUNE)
val_ds = raw_val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = raw_test_ds.prefetch(buffer_size=AUTOTUNE)

input_shape = IMAGE_SIZE + (IMAGE_CHANNELS,)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
base_model.trainable = False

model = models.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(ROTATION_FACTOR),
    layers.RandomBrightness(factor=BRIGHTNESS_FACTOR),
    layers.RandomContrast(factor=CONTRAST_FACTOR),
    # Note: 1./127.5, offset=-1 scales pixels to [-1, 1] specifically for MobileNetV2
    layers.Rescaling(1./127.5, offset=-1),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(DROPOUT_RATE),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
print("Phase 1: Training the Head...")
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=PHASE_1_EPOCHS,
    class_weight=class_weights
)

print("Phase 2: Fine-Tuning...")
base_model.trainable = True
for layer in base_model.layers[:-FINE_TUNE_LAYERS]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=FINE_TUNE_LR),
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy']
)

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', 
    patience=EARLY_STOP_PATIENCE, 
    restore_best_weights=True
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=f"server/models/{training_model_name}.keras",
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)

lr_reducer = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=2,
    min_lr=1e-7,
    verbose=1
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=PHASE_2_EPOCHS,
    callbacks=[early_stop, checkpoint, lr_reducer],
    class_weight=class_weights
)

print("\n=== Evaluating on Unseen Test Data ===")
best_model = tf.keras.models.load_model(f"server/models/{training_model_name}.keras")

loss, accuracy = best_model.evaluate(test_ds)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {(accuracy * 100):.2f}%")