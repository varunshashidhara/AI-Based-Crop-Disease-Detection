import os
import shutil
import random

# Paths
BASE_DIR = r"C:\Users\Lenovo\OneDrive\Desktop\ai-crop-disease\backend\app\Data"
SOURCE_DIR = os.path.join(BASE_DIR, "train")
DEST_TRAIN = os.path.join(BASE_DIR, "data", "train")
DEST_VAL = os.path.join(BASE_DIR, "data", "val")

# Train/validation split ratio
SPLIT_RATIO = 0.8

def prepare_folders():
    os.makedirs(DEST_TRAIN, exist_ok=True)
    os.makedirs(DEST_VAL, exist_ok=True)

def split_dataset():
    classes = [d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))]

    for cls in classes:
        cls_path = os.path.join(SOURCE_DIR, cls)
        images = os.listdir(cls_path)
        random.shuffle(images)

        split_idx = int(len(images) * SPLIT_RATIO)
        train_imgs = images[:split_idx]
        val_imgs = images[split_idx:]

        # Create destination folders
        train_cls_dir = os.path.join(DEST_TRAIN, cls)
        val_cls_dir = os.path.join(DEST_VAL, cls)
        os.makedirs(train_cls_dir, exist_ok=True)
        os.makedirs(val_cls_dir, exist_ok=True)

        # Move images
        for img in train_imgs:
            shutil.copy(os.path.join(cls_path, img), os.path.join(train_cls_dir, img))
        for img in val_imgs:
            shutil.copy(os.path.join(cls_path, img), os.path.join(val_cls_dir, img))

        print(f"Class {cls}: {len(train_imgs)} train, {len(val_imgs)} val")

if __name__ == "__main__":
    prepare_folders()
    split_dataset()
    print("✅ Dataset successfully split into train/ and val/")
