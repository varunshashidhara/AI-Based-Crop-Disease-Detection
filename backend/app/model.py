import os
import json
import numpy as np
from PIL import Image
from .config import settings

class ModelHandler:
    def __init__(self):
        self.model = None
        self.class_names = []
        self.advice_dict = {}
        
        # Load Advice Dict
        try:
            if os.path.exists(settings.disease_info_path):
                with open(settings.disease_info_path, "r") as f:
                    self.advice_dict = json.load(f)
            else:
                print(f"Warning: {settings.disease_info_path} not found.")
        except Exception as e:
            print(f"Error loading advice dictionary: {e}")
        
        # Load Class Indices
        try:
            if os.path.exists(settings.class_indices_path):
                with open(settings.class_indices_path, "r") as f:
                    class_indices = json.load(f)
                # Reverse mapping: index -> class label
                index_to_class = {v: k for k, v in class_indices.items()}
                # Ensure the class_names list is ordered correctly by index
                self.class_names = [index_to_class[i] for i in range(len(index_to_class))]
                print(f"Loaded {len(self.class_names)} classes from {settings.class_indices_path}")
            else:
                print(f"Warning: {settings.class_indices_path} not found. Running with empty classes.")
        except Exception as e:
            print(f"Error loading class indices: {e}")

        # Load Model
        try:
            from tensorflow.keras.models import load_model
            model_to_load = None
            if os.path.exists(settings.model_path_final):
                model_to_load = settings.model_path_final
            elif os.path.exists(settings.model_path):
                model_to_load = settings.model_path
                
            if model_to_load:
                self.model = load_model(model_to_load)
                print('Loaded model from', model_to_load)
            else:
                print(f'No model found at {settings.model_path_final} or {settings.model_path}. Running in demo mode.')
        except Exception as e:
            print('TensorFlow not available or failed to load model:', e)
            self.model = None

    def predict_pil(self, pil_image):
        if self.model is None or not self.class_names:
            return {
                'label': 'Unknown_Disease (demo)',
                'confidence': 0.0,
                'advice': 'Train model and ensure both .keras model and class_indices.json are present in backend/app/'
            }

        img = pil_image.resize((224, 224))
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0) # Add batch dimension
        
        preds = self.model.predict(arr)
        idx = int(np.argmax(preds, axis=1)[0])
        confidence = float(np.max(preds))
        
        label = self.class_names[idx] if idx < len(self.class_names) else f'class_{idx}'
        
        disease_info = self.advice_dict.get(label, {})
        advice = disease_info.get('advice', 'Consult an agricultural expert for this disease.')

        res = {'label': label, 'confidence': confidence, 'advice': advice}
        if 'name' in disease_info:
            res['clean_name'] = disease_info['name']
        if 'crop' in disease_info:
            res['crop'] = disease_info['crop']
            
        return res
