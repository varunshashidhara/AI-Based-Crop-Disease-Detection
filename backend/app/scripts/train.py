import os
import signal
import sys
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.applications import MobileNetV2

# -----------------------------
# SETTINGS
# -----------------------------
DATA_DIR = "../Data"           
MODEL_PATH = "../crop_disease_model_final.keras"
LABELS_PATH = "../class_indices.json"
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
# SAVE CLASS INDICES
# -----------------------------
os.makedirs("..", exist_ok=True)  # ensure folder exists
with open(LABELS_PATH, "w") as f:
    json.dump(train_generator.class_indices, f, indent=4)
print(f"✅ Saved class indices at {LABELS_PATH}")

# -----------------------------
# MODEL DEFINITION
# -----------------------------
if os.path.exists(MODEL_PATH):
    print("🔄 Loading existing model...")
    model = load_model(MODEL_PATH)
    initial_epoch = int(model.optimizer.iterations.numpy() // len(train_generator))
else:
    print("✨ Creating new MobileNetV2 transfer learning model...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SIZE + (3,))
    
    # Freeze the base model
    base_model.trainable = False

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(len(train_generator.class_indices), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    initial_epoch = 0

print("Class labels:", train_generator.class_indices)

# -----------------------------
# CHECKPOINT & EARLY STOPPING CALLBACK
# -----------------------------
checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True,
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
    callbacks=[checkpoint, early_stopping]
)

print("✅ Training complete. Model saved at:", MODEL_PATH)

