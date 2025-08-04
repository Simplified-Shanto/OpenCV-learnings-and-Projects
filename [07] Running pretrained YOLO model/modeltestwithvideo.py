from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolo_output/weights/best.pt")

cap = cv2.VideoCapture("Test samples/Indian_traffic_sign.mp4")

while True:
    success, frame = cap.read()

    prediction = model.predict(frame)[0]
    prediction = prediction.plot(line_width=2)
    prediction = prediction[:, :, ::-1]
    prediction = Image.fromarray(prediction)
    prediction.save("output_image.png")

    outputImage = cv2.imread("output_image.png")

    scale_factor = 0.5
    resized_image = cv2.resize(outputImage, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    cv2.imshow("Output", resized_image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break