import numpy as np
import cv2


###########################################
widthImg = 480
heightImg = 640
##########################################
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




cap = cv2.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10, 150)

def getContours(img):
    biggestContour = np.array([]) #Our initial biggest contour
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >  3000:  # avoiding tiny noiselike contours
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # In this part we try to find the area possible and update
            # the contour variable to get the biggest contour
            # and len(approx) == 4 -> ensures that we only check the contours having 4 corner
            # points
            if area > maxArea and len(approx) == 4:
                biggestContour = approx  # Assigning the current contour as the biggest contour
                maxArea = area    # Updating the max area of contour with the area of the
                                  # the current contour
    cv2.drawContours(imgContour, biggestContour, -1, (255, 0, 0), 20)
    return biggestContour


def reorder (myPoints):
    original_Points = myPoints.copy()
    myPointsNew = np.zeros((4, 1, 2), np.int32)

    myPoints = myPoints.reshape(8)
    print("myPoints", myPoints)
    pointsX = [myPoints[0]]
    pointsY = [myPoints[1]]
    pointsX.append(myPoints[2])
    pointsY.append(myPoints[3])
    pointsX.append(myPoints[4])
    pointsY.append(myPoints[5])
    pointsX.append(myPoints[6])
    pointsY.append(myPoints[7])
    print("pointsX", pointsX)


    myPointsNew[0] = original_Points[np.argmin(pointsX)]
    myPointsNew[3] = original_Points[np.argmax(pointsX)]
    myPointsNew[1] = original_Points[np.argmin(pointsY)]
    myPointsNew[2] = original_Points[np.argmax(pointsY)]
    # sum_array = myPoints.sum(1)
    # print(sum_array)
    # # np.argmin(add) returns the index of the smallest
    # # element in the array "add"
    # myPointsNew[0] = myPoints[np.argmin(sum_array)]
    # myPointsNew[3] = myPoints[np.argmax(sum_array)]
    # difference_array = np.diff(myPoints, axis = 1)
    # myPointsNew[2] = myPoints[np.argmin(difference_array)]
    # myPointsNew[1] = myPoints[np.argmax(difference_array)]
    return myPointsNew


def getWarp(img, biggest):
    print("raw Biggest")
    print(biggest)
    biggest  = reorder(biggest)
    print("Reordered Biggest")
    print(biggest)
    # The current four corners of the image input
    pts1 = np.float32(biggest)
    # The desired four corner positions of the output image
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    imgCropped = imgOutput
    #imgCropped = imgOutput[0:imgOutput.shape[0], 40:imgOutput.shape[1]]
    return imgCropped



# def preProcessing(img):
#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     #undo the blurring process if things don't work
#     #imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
#     imgBlur = img
#     imgCanny = cv2.Canny(imgGray, 200, 200)
#     # Following code makes the boundries much thicker facilitating
#     # detection
#     kernel = np.ones((5, 5))
#     imgDilated = cv2.dilate(imgCanny, kernel, iterations = 2)
#     imgThres = cv2.erode(imgDilated, kernel, iterations = 1)
#     return imgThres



while True:
    #Reading images from the webcam stream.
    success, img =cap.read()

    img = cv2.flip(img, 1)  # Flipping the image horizontally
    # as we get horizontally flipped
    # image from our webcam
    #img = cv2.imread("Resources/book.jpg")
    img_resized = cv2.resize(img, (heightImg, heightImg))
    imgContour  = img_resized.copy()
    imgGray     = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # undo the blurring process if things don't work
    #imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgBlur     = imgGray
    imgCanny    = cv2.Canny(imgBlur, 200, 200)
    # Following code makes the boundries much thicker facilitating
    # detection
    kernel = np.ones((5, 5))
    imgDilated  = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres    = cv2.erode(imgDilated, kernel, iterations=1)
    #imgThres = preProcessing(img_resized)
    biggest = getContours(imgThres)
    #print(biggest)
    if biggest.size ==0:
        imgWarped = imgThres
        imgContour = imgCanny
    else:
        imgWarped   = getWarp(img, biggest)

    stackedImages = stackImages(0.3,([img_resized, imgGray, imgBlur, imgCanny],
                                                [imgContour, imgDilated, imgThres, imgWarped]))
    cv2.imshow("Warped Image", imgWarped)
    cv2.imshow("Workflow", stackedImages)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break