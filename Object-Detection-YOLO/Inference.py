import tensorflow as tf
import numpy as np
import os
import cv2


modelPath = 'Models/YoloEfficientNetUntrained.keras'
trainedModelPath = 'Models/checkpoints/YoloEfficientNet.keras'
model = tf.keras.models.load_model(modelPath)
model.load_weights(trainedModelPath)

B = 2
NUM_CLASSES = 20
NUM_FILTERS = 512
OUTPUT_DIM = NUM_CLASSES + 5*B
H, W = 224, 224
SPLIT_SIZE = H//32
BATCH_SIZE = 32

classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 
            'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 
            'train', 'tvmonitor']

def testModel(frame, originalSize):
    try:
        originalH, originalW = originalSize
        # Resize the captured frame to match the model's input size
        image = cv2.resize(frame, (H, W))
        image_tensor = tf.convert_to_tensor(image, dtype=tf.float32)
        image_tensor = tf.image.resize(image_tensor, [H, W])

        # Model prediction
        output = model.predict(np.expand_dims(image_tensor, axis=0))

        THRESH = 0.25
        objectPositions = tf.concat(
            [tf.where(output[..., 0] >= THRESH), tf.where(output[..., 5] >= THRESH)], axis=0)
        selectedOutput = tf.gather_nd(output, objectPositions)

        if len(objectPositions) == 0:
            return frame

        finalBoxes = []
        finalScores = []

        for i, pos in enumerate(objectPositions):
            for j in range(2):
                if selectedOutput[i][j * 5] > THRESH:
                    outputBox = tf.cast(output[pos[0]][pos[1]][pos[2]][(j * 5) + 1:(j * 5) + 5], dtype=tf.float32)

                    xCentre = (tf.cast(pos[1], dtype=tf.float32) + outputBox[0]) * 32
                    yCentre = (tf.cast(pos[2], dtype=tf.float32) + outputBox[1]) * 32
                    width = tf.math.abs(H * outputBox[2])
                    height = tf.math.abs(W * outputBox[3])

                    xMin, yMin = int(xCentre - width / 2), int(yCentre - height / 2)
                    xMax, yMax = int(xCentre + width / 2), int(yCentre + height / 2)

                    xMin = max(0, xMin)
                    xMax = min(W, xMax)
                    yMin = max(0, yMin)
                    yMax = min(H, yMax)

                    finalBoxes.append([xMin, yMin, xMax, yMax,
                                       str(classes[tf.argmax(selectedOutput[..., 10:], axis=-1)[i]])])
                    finalScores.append(selectedOutput[i][j * 5])
        
        if len(finalBoxes)==0:
            return frame

        finalBoxes = np.array(finalBoxes)

        objectClasses = finalBoxes[..., 4]
        nmsBoxes = finalBoxes[..., 0:4]

        nmsOutput = tf.image.non_max_suppression(
            nmsBoxes, finalScores, max_output_size=100, iou_threshold=0.2,
            score_threshold=float('-inf')
        )

        # Draw bounding boxes on the frame
        for i in nmsOutput:
            cv2.rectangle(
                image,
                (int(finalBoxes[i][0]), int(finalBoxes[i][1])),
                (int(finalBoxes[i][2]), int(finalBoxes[i][3])), (0, 0, 255), 2
            )
            cv2.putText(
                image,
                finalBoxes[i][-1],
                (int(finalBoxes[i][0]), int(finalBoxes[i][1]) + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )
        image = cv2.resize(image, (originalW, originalH))
        return image  # Return the frame with detections
    except Exception as e:
        print(f'Error processing frame: {str(e)}')

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()  # Capture frame
    if not ret:
        break

    originalSize = (frame.shape[0], frame.shape[1])

    # Get bounding boxes from YOLO
    output = testModel(frame, originalSize)

    cv2.imshow('YOLO Detection', output)  # Show real-time detection

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
