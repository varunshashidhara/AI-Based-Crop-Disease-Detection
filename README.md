# 🌱 AI-Based Crop Disease Detection

A full-stack, AI-powered web application that instantly diagnoses plant leaf diseases and provides actionable agricultural advice. This tool bridges the gap between deep learning algorithms and everyday farming utility, helping agronomists, farmers, and home gardeners optimize their agricultural yields.

---

## 🚀 Features

- **Real-Time AI Diagnosis:** Upload a photo of a crop leaf and the system identifies diseases with high accuracy using a deep learning model.
- **Actionable Agricultural Advice:** The system dynamically queries a customized knowledge base (`disease_info.json`) to provide specific treatment plans.
- **Premium User Interface:** A modern, visually stunning "glassmorphic" frontend featuring an intuitive drag-and-drop zone with animated feedback.
- **Robust API Backend:** Powered by FastAPI for lightning-fast inference and solid security, including complete file-type validation.
- **Cloud Ready:** A complete `Dockerfile` is included, meaning the backend can be instantly deployed to Render, AWS, Google Cloud, or Heroku.

---

## 🧠 Machine Learning Architecture

The AI engine utilizes **Transfer Learning** built upon the **MobileNetV2** architecture. 

By taking a model pre-trained on the massive ImageNet dataset, we fine-tune the dense output layers specifically on agricultural leaf structures. MobileNetV2 was explicitly chosen for its optimal balance of high classification accuracy and lightweight computational footprint, making it perfect for rapid, real-time web inference.

The training pipeline integrates features such as `ImageDataGenerator` for robust data augmentation and `EarlyStopping` to prevent model overfitting.

---

## 🛠️ Tech Stack

### Frontend
- **HTML5 & CSS3:** Semantic markup styled via a standalone `styles.css` file utilizing modern Glassmorphism, CSS variables, grid, flexbox, and CSS micro-animations.
- **Vanilla JavaScript (`app.js`):** Asynchronous Javascript managing drag-and-drop validation, loading states, and REST API communication.

### Backend
- **Python 3.10+**
- **FastAPI:** High-performance web framework used for handling POST uploads and predictions.
- **Uvicorn:** Lightning-fast ASGI web server implementation used for Python.
- **TensorFlow & Keras:** Building, training, and running inference on the MobileNetV2 CNN.
- **Pydantic:** Managing application configuration environments elegantly.
- **Docker:** OS-level virtualization to deliver software in standardized packages called containers.

---

## 📁 Project Structure

```text
AI-Based-Crop-Disease-Detection/
│
├── frontend/                     # Premium Web User Interface
│   ├── index.html                # Main interface markup
│   ├── styles.css                # Glassmorphic and responsive styling
│   └── app.js                    # UI logic and API networking
│
├── backend/                      # Python FastAPI Application
│   ├── app/                      
│   │   ├── main.py               # FastAPI entry point & routes (/predict, /health)
│   │   ├── model.py              # TensorFlow inference handler and advice mapping
│   │   ├── config.py             # Pydantic environment configurations
│   │   ├── disease_info.json     # Centralized agricultural advice matrix
│   │   └── scripts/              # Neural Network Training Scripts
│   │       ├── train.py          # MobileNetV2 Transfer Learning pipeline
│   │       └── dataset_splitter.py
│   ├── Dockerfile                # Containerization setup
│   └── requirements.txt          # Python dependencies
│
└── .gitignore                    # Excludes heavy ML models (.keras) and venvs
```

---

## 💻 Local Setup & Development

Follow these steps to spin up the application on your local machine.

### 1. Requirements
Ensure you have Python 3.9+ installed and Git available on your terminal.

### 2. Clone the Repository
```bash
git clone https://github.com/varunshashidhara/AI-Based-Crop-Disease-Detection.git
cd AI-Based-Crop-Disease-Detection/backend
```

### 3. Setup Virtual Environment & Install Dependencies
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On MacOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
pip install pydantic-settings
```

### 4. Provide the AI Model
Because compiled AI models (`.keras` / `.h5` files) are massive, they are not tracked via GitHub. You must place your trained `crop_disease_model_final.keras` and the generated `class_indices.json` into the `backend/app/` folder before running.

*If you do not have a model, you can train one by running `python app/scripts/train.py` (ensure you have a dataset under `backend/Data/`).*

### 5. Start the FastAPI Server
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
You can verify the API is running by visiting `http://127.0.0.1:8000/health`.

### 6. Run the Frontend
Simply double-click the `frontend/index.html` file to open it in your browser. Drag and drop any crop leaf image to test the detection!

---

## 🐳 Docker Deployment

To build and run the backend inside a Docker container:
```bash
cd backend
docker build -t crop-disease-api .
docker run -p 8000:8000 crop-disease-api
```

---

## 📝 License
This project is open-source and available under the MIT License.

Developed by Varun S
