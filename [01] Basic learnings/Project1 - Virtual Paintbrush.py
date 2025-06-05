import numpy as np
import cv2


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def getContours(img):
    x, y, w, h = 0, 0, 0, 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area >  1000:  # avoiding tiny noiselike contours
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y , w, h = cv2.boundingRect(approx)
    return x+w//2, y

# Mycolors is the list of colors that we want to detect
myColors = [
        [19, 58, 177, 40, 168, 255],     #yellow heatshrink
    [145, 131, 110, 179, 255, 255],    #Red heatshrink
    [70, 108, 88, 98,255,  255]     #Green color pen head
]
myColorValues = [ # Format is BGR
                 [0,100, 100  ], #YELLOW color
                 [0, 0  , 250], #Red color
                 [0 , 250, 0  ]  #Green color
                 ]

myPoints =   []   # [x, y, colorID]

# We'll use this function to find our color
def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0   # goes through all the 3 color set we have
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x!= 0 and y!= 0:
            newPoints.append([x, y, count])
        cv2.imshow("Mask", mask)
        count+=1
    return newPoints


def drawOnCanvas(pointsArray, colorValues):
    for point in pointsArray:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)



frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)


while True:
    # Reading images from the webcam stream.
    success, img =cap.read()
    img = cv2.flip(img, 1) #Flipping the image horizontally
                                    #as we get horizontally flipped
                                    #image from our webcam
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints)!= 0:
        for newPoint in newPoints:
            myPoints.append(newPoint) # Adding the points we just drawn
                                      # to the set of all points which
                                      # will be drawn over and over again

    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Image", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break