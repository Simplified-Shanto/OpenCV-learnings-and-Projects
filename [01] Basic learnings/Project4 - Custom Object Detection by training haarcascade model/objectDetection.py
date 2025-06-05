import cv2

########################################################
path = 'Haarcascades/haarcascade_frontalface_default.xml' # PATH OF THE CASCADE
cameraNo = 0               # Camera number
objectName = 'FACE'        # Name of the object to display
frameWidth = 640
frameHeight = 480
color = (255, 0, 255)
#########################################################


# Camera parameters

cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

# Create TrackBAr
cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight + 100)
cv2.createTrackbar("Scale", "Result", 400, 1000, empty)
cv2.createTrackbar("Neighbour", "Result", 8, 20, empty)
cv2.createTrackbar("Min Area", "Result", 0, 10000, empty)
cv2.createTrackbar("Brightness", "Result", 180, 255, empty)

# Load the particular classifier from the folder
cascade = cv2.CascadeClassifier(path)

while True:
    # SET camera brightness from trackbar value
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, cameraBrightness)
    #Get camera image and convert to grayscale
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the object using the cascade
    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "Result")/1000)
    neighbour = cv2.getTrackbarPos("Neighbour", "Result")
    objects = cascade.detectMultiScale(imgGray, scaleVal, neighbour)
    # Display the detected objects
    for(x, y, w, h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y+h), color, 3)
            cv2.putText(img, objectName, (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            #Roi = Region of Interest,
            roi_color = img[y:y+h, x:x+w]
    cv2.imshow("Result", img)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break
