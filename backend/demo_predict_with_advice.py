import os
import sys
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# -----------------------------
# SETTINGS
# -----------------------------
MODEL_PATH = "app/crop_disease_model_final.keras"
CLASS_INDICES_PATH = "app/class_indices.json"
DISEASE_INFO_PATH = "app/disease_info.json"
IMG_SIZE = (224, 224)

# -----------------------------
# LOAD ADVICE DICT
# -----------------------------
advice_dict = {}
if os.path.exists(DISEASE_INFO_PATH):
    with open(DISEASE_INFO_PATH, "r") as f:
        advice_dict = json.load(f)
else:
    print(f"Warning: '{DISEASE_INFO_PATH}' not found.")

# -----------------------------
# GET IMAGE PATH FROM ARGUMENT
# -----------------------------
if len(sys.argv) < 2:
    print("Usage: python demo_predict_with_advice.py <image_path>")
    sys.exit(1)

img_path = sys.argv[1]
if not os.path.exists(img_path):
    print(f"Error: File '{img_path}' does not exist.")
    sys.exit(1)

# -----------------------------
# LOAD MODEL
# -----------------------------
print("Loading model...")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully.")

# -----------------------------
# LOAD CLASS INDICES
# -----------------------------
if not os.path.exists(CLASS_INDICES_PATH):
    print(f"Error: '{CLASS_INDICES_PATH}' not found. Make sure you saved class_indices.json during training.")
    sys.exit(1)

with open(CLASS_INDICES_PATH, "r") as f:
    class_indices = json.load(f)

# Reverse mapping: index -> class label
index_to_class = {v: k for k, v in class_indices.items()}
print("Class labels:", list(index_to_class.values()))

# -----------------------------
# PREPROCESS IMAGE
# -----------------------------
img = image.load_img(img_path, target_size=IMG_SIZE)
img_array = image.img_to_array(img) / 255.0  # rescale like training
img_array = np.expand_dims(img_array, axis=0)

# -----------------------------
# PREDICT
# -----------------------------
pred_probs = model.predict(img_array)
pred_index = np.argmax(pred_probs, axis=1)[0]
pred_class = index_to_class[pred_index]

print(f"Predicted class: {pred_class}")

# -----------------------------
# PROVIDE ADVICE
# -----------------------------
disease_info = advice_dict.get(pred_class, {})
advice = disease_info.get("advice", "No advice available for this class.")
print(f"Suggested action for farmer: {advice}")
