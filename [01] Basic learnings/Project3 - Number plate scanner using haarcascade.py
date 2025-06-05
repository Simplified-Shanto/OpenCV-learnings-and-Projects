import cv2
import numpy as np

# These cascade files (like haarcascade_frontalface_default.xml)
# are pretrained classifiers stored in XML format. OpenCV ships
# with several—for face, eyes, smile, etc.




###########################################
widthImg = 480
heightImg = 640
numberPlateCascade = cv2.CascadeClassifier("Resources/haarcascades/haarcascade_russian_plate_number.xml")
minArea = 500
color = (255, 0, 255)
count = 0
##########################################


cap = cv2.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10, 150)

while 1:
    success, img = cap.read()
    imageGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgRoi = img.copy()

    numberPlates = numberPlateCascade.detectMultiScale(imageGray, 1.1, 4)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(img, "NumberPlate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color)
            #Roi = Region of interest, the number plate, we'll save it.
            imgRoi = img[y:y+h, x:x + w]
            cv2.imshow("Number Plate" , imgRoi)
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            print(count)
            count+=1
            cv2.imwrite("Resources/Scans/NoPlate_"+str(count) + ".jpg", imgRoi)
            cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 200), 2)
            cv2.imshow("Result", img)
            cv2.waitKey(500)



