import onnxruntime
import cv2
import numpy as np
import time
import service.main as s
def emotionDetector(image):
    classNames = ["angry", "happy", "sad"]

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    image = cv2.resize(image, (224, 224))
    image = np.float32(image)
    image = np.expand_dims(image, axis=0)

    startTime = time.time()

    predictions = s.session.run(['dense'], {"image": image})
    emotion =  classNames[np.argmax(predictions[0])]

    timeElapsed = time.time() - startTime

    return {'emotion' : emotion, 'probability' : np.max(predictions[0]), 'timeElapsed' : timeElapsed}


