from pydantic import BaseModel

class EmotionOutput(BaseModel):
    emotion: str
    probability: float
    timeElapsed: float