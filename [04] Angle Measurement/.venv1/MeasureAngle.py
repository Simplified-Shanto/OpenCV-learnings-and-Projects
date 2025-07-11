import cv2
import numpy as np
import os
import math

from numpy.ma.core import arctan

pointsList = []
path = "360protractor.jpg"
frame = cv2.imread(path)
frame_copy = cv2.imread(path)


def mousePoints(event, x, y, flags, params):
    global frame  # <-- Add this line
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pointsList) == 3:
            pointsList.clear()
            frame = cv2.imread(path)
        pointsList.append((x, y))
        print(pointsList)

def slope(point1, point2): # / -> Normal division // -> Floor division
    return (point2[1] - point1[1])/(point2[0] - point1[0])


def measureAngle(p1, p2, p3):
    # Convert points to vectors: A = p1 → p2, B = p3 → p2 (reverse B for correct orientation)
    A = (p1[0] - p2[0], p1[1] - p2[1])
    B = (p3[0] - p2[0], p3[1] - p2[1])

    # Dot product and magnitude
    dot = A[0] * B[0] + A[1] * B[1]
    magA = math.hypot(A[0], A[1])
    magB = math.hypot(B[0], B[1])

    # Get the angle in radians
    angle = math.acos(dot / (magA * magB))

    # Cross product (for direction)
    cross = A[0] * B[1] - A[1] * B[0]

    # Convert to degrees
    angle_deg = math.degrees(angle)

    # # Determine reflex direction (clockwise vs counter-clockwise)
    # if cross < 0:
    #     angle_deg = 360 - angle_deg

    return angle_deg

while True:
    cv2.imshow("Image", frame)
    cv2.setMouseCallback('Image', mousePoints)

    for point in pointsList:
        cv2.circle(frame, (point[0], point[1]), 3, (200, 100, 0), cv2.FILLED)
        if len(pointsList) ==2:
            cv2.line(frame, pointsList[0], pointsList[1], (100, 200, 0), 2)
        if len(pointsList) ==3:
            cv2.line(frame, pointsList[1], pointsList[2], (100, 200, 0), 2)
            angle = measureAngle(pointsList[0], pointsList[1], pointsList[2])
            cv2.putText(frame, str(round(angle)), (pointsList[1][0] - 30, pointsList[1][1] + 30),1,  color = (255, 100, 0), thickness = 2, fontScale=2)
            """fontFace: This parameter specifies the font type to be used for rendering the text. OpenCV provides a set of predefined Hershey Fonts, which are vector fonts suitable for various applications. Examples include cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX, etc. You select the desired font by passing its corresponding constant to this parameter.
            fontScale: This parameter is a scale factor that determines the size of the text. It acts as a multiplier for the base size of the chosen fontFace. A higher fontScale value results in larger text, while a lower value makes the text smaller. This allows you to adjust the text size to fit your image and visual requirements.
            """



    cv2.waitKey(1)
