import cv2
import os
import time

#############################################

myPath = 'data/images'
cameraNo = 0
cameraBrightness = 190
imageInterval = 10 # Save the ith frame to avoid repetition
               # imgaeInterval = 10 means we will be saving every
               # 10th frame
maxBlur = 500 # If the image is too blury, it'll hinder the training process,
              # , so if the blurriness value is above 500, we won't save it
grayImage = False # Whether images are saved colored or gray
saveData = True   # Save Data Flag
showImage = True  # Whether data is saved or not
imgWidth  = 180
imgHeight = 120

##############################################

global CountFolder
cap = cv2.VideoCapture(cameraNo)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, cameraBrightness)

count = 0
countSave = 0

def saveDataFunc():
    global folderCount
    folderCount = 0
    # If the folder with that particular count already exists, then
    # increase the folder count number to create a new folder
    while os.path.exists(myPath + str(folderCount)):
        folderCount = folderCount + 1
    os.makedirs(myPath + str(folderCount))

if saveData == True:
    saveDataFunc()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (imgWidth, imgHeight))

    if grayImage:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if saveData:
        blur = cv2.Laplacian(img, cv2.CV_64F).var()
        if count % imageInterval == 0 and blur > maxBlur:
            nowTime = time.time()
            cv2.imwrite(myPath + str(folderCount)
            + '/' + str(countSave) + " " + str(int(blur)) + "_" +
            str(nowTime) + ".png", img)
            countSave+=1
        count+=1

    if showImage:
        cv2.imshow("Image", img)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cap.closeAllWindows()






