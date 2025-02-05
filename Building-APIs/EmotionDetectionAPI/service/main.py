from fastapi import FastAPI
from service.api.api import apiRouter
import onnxruntime

app = FastAPI(project_name="Emotion Detection API")
app.include_router(apiRouter)

providers = ['CPUExecutionProvider']
session = onnxruntime.InferenceSession("service/EmotionDetectionViT.onnx", providers=providers)

@app.get("/")
async def root():
    return {'Hello' : 'World'}