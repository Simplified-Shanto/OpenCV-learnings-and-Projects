import cv2
import time
import poseModule as pm

cap = cv2.VideoCapture('testvideo0.mp4')
previousTime = 0
detector = pm.poseDetector()

while True:
    success, img = cap.read()  # image is in BGR format
    img = detector.findPose(img, draw = True)
    lmList = detector.getPosition(img, draw = True)
    #print(lmList[14])
    #cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 200), cv2.FILLED) # In case you want to track a single landmark
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
