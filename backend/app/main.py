# backend/app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .model import ModelHandler
from PIL import Image
import io

app = FastAPI(title="AI Crop Disease Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = ModelHandler()

@app.get('/')
@app.get('/health')
async def health_check():
    return JSONResponse(content={"success": True, "message": "API is running."})

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        return JSONResponse(status_code=400, content={"success": False, "error": "File uploaded is not an image."})
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        result = model.predict_pil(image)
        return JSONResponse(content={"success": True, "prediction": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
