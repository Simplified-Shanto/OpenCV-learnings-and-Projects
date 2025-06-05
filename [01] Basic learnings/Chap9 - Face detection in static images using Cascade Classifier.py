import numpy as np
import cv2
path = 'Resources/people.jpg'
# These cascade files (like haarcascade_frontalface_default.xml)
# are pretrained classifiers stored in XML format. OpenCV ships
# with several—for face, eyes, smile, etc.
faceCascade = cv2.CascadeClassifier("Resources/haarcascades/haarcascade_frontalface_default.xml")
#Reading the image
image = cv2.imread(path)
# Converting the image to GrayScale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(imageGray, 1.1, 4)
for (x, y, w, h)  in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)


cv2.imshow("Image", image)
cv2.waitKey(0)