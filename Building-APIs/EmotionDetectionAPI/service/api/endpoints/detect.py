from fastapi import APIRouter, UploadFile, HTTPException
from PIL import Image
from io import BytesIO
import numpy as np
from service.core.logic.onnxInference import emotionDetector
from service.core.schemas.output import EmotionOutput

emoRouter = APIRouter()

@emoRouter.post("/detect", response_model=EmotionOutput)
async def detect(im : UploadFile):

    if im.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    image = Image.open(BytesIO(im.file.read()))
    image = np.array(image)
    return emotionDetector(image)