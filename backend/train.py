import os
import signal
import sys
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

# -----------------------------
# SETTINGS
# -----------------------------
DATA_DIR = "app/Data"                       # Main dataset folder
MODEL_PATH = "app/crop_disease_model.keras" # Modern Keras format
LABELS_PATH = "app/class_indices.json"      # Save class indices for demo
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
TOTAL_EPOCHS = 15
VALIDATION_SPLIT = 0.2

# -----------------------------
# DATA GENERATORS
# -----------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=VALIDATION_SPLIT,
    horizontal_flip=True,
    rotation_range=20,
    zoom_range=0.2
)

train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# -----------------------------
# MODEL DEFINITION
# -----------------------------
if os.path.exists(MODEL_PATH):
    print("🔄 Loading existing model...")
    model = load_model(MODEL_PATH)
    initial_epoch = int(model.optimizer.iterations.numpy() // len(train_generator))
else:
    print("✨ Creating new model...")
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=IMG_SIZE + (3,)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(train_generator.class_indices), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    initial_epoch = 0

# Save class indices for demo
with open(LABELS_PATH, "w") as f:
    json.dump(train_generator.class_indices, f)

print("Class labels:", train_generator.class_indices)

# -----------------------------
# CHECKPOINT CALLBACK
# -----------------------------
checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor='val_accuracy',
    save_best_only=False,
    save_weights_only=False,
    verbose=1
)

# -----------------------------
# INTERRUPT HANDLING
# -----------------------------
def handle_sigint(sig, frame):
    print("\n⏹ Training interrupted. Saving model...")
    model.save(MODEL_PATH)
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

# -----------------------------
# TRAIN MODEL
# -----------------------------
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=TOTAL_EPOCHS,
    initial_epoch=initial_epoch,
    callbacks=[checkpoint]
)

print("✅ Training complete. Model saved at:", MODEL_PATH)

