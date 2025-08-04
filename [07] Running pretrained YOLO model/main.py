from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolo_output/weights/best.pt")

imageIndex = 5260
resized_image = cv2.imread("Dataset/images/IMG_5260.JPG")

while True:
    cv2.imshow("Output", resized_image)
    key = cv2.waitKey(1)
    if key==ord('q'):
        break
    elif key==ord('n'): # n = go to next test image
        imageIndex = imageIndex + 5
        try:
            try: # In our test sample we have both .JPG and .jpeg extensions
                testImage = cv2.imread(f"Dataset/images/IMG_{imageIndex}.JPG")
            except:
                testImage = cv2.imread(f"Dataset/images/IMG_{imageIndex}.jpeg")
        except:
            imageIndex = imageIndex + 1
            pass


        prediction = model.predict(testImage)[0]
        prediction = prediction.plot(line_width=1)
        prediction = prediction[:, :, ::-1]
        prediction = Image.fromarray(prediction)
        prediction.save("output_image.png")

        outputImage = cv2.imread("output_image.png")

        scale_factor = 0.5
        resized_image = cv2.resize(outputImage, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    # elif key == ord('p'): # p = go the previous test image
    #     imageIndex = imageIndex - 1
    #
    #     testImage = cv2.imread(f"Dataset/images/IMG_{imageIndex}.jpeg")
    #
    #     prediction = model.predict(testImage)[0]
    #     prediction = prediction.plot(line_width=1)
    #     prediction = prediction[:, :, ::-1]
    #     prediction = Image.fromarray(prediction)
    #     prediction.save("output_image.png")
    #
    #     outputImage = cv2.imread("output_image.png")
    #
    #     scale_factor = 0.3
    #     resized_image = cv2.resize(outputImage, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    #     cv2.imshow("Output", resized_image)

    #print("Working")