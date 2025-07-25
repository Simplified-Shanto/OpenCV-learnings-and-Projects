import math
import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector #The purpose of the Python library CVZone is to simplify and accelerate the development of computer vision projects. It acts as a high-level abstraction built upon powerful libraries like OpenCV and MediaPipe, making complex computer vision tasks more accessible to both beginners and experienced developers.
import random
detector = HandDetector(detectionCon=0.8, maxHands=1) #detectionCon = detection Confidence

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #cv2.VideoCapture(0) — What's happening? This grabs the default camera (usually your webcam) using OpenCV’s default backend (the system decides which one to use, like DirectShow, MSMF, etc.).
# cv2.VideoCapture(0, cv2.CAP_DSHOW) — What’s different? Now you’re explicitly telling OpenCV to use DirectShow (a Windows video capture API) to access the webcam.
#⚠️ When not to use it? If you’re on Linux or Mac, this will break (DirectShow is Windows-only)
cap.set(3, 1280)
cap.set(4, 720)
pathFood = "Donut.png"


class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = [] #list of all points of the snake structure
        self.lengths = [] # distance between each point
        self.current_length = 0 # total length of the snake
        self.allowedLength = 200 # total allowed length This is the initial length of the snake, and the length will grow further after eating food
        self.previousHead = 0, 0 # coordinate of the previous head
        self.score = 0

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED) # the second parameter is used to preserve the transparency (aka alpha channel) of the image, using it loads all the 4 channles R, G, B, A  and without it, the alpha channel is dropped
        self.food_height, self.food_width, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint =  random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver == True:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400], 7, 5,offset = 20)
            cvzone.putTextRect(imgMain, f"Score = {self.score}", [300, 200], 7, 5, offset=20)
        else:
            previous_x, previous_y = self.previousHead
            current_x , current_y  = currentHead

            self.points.append([current_x, current_y])
            distance = math.hypot(current_x - previous_x, current_y - previous_y)
            self.lengths.append(distance)
            self.current_length+=distance
            self.previousHead = current_x, current_y

            # Length Reduction
            if self.current_length > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.current_length -= length
                    self.lengths.pop(i) # Removing the reduced length from the lengths list
                    self.points.pop(i)
                    if self.current_length < self.allowedLength:
                        break

            # check if snake ate the food
            food_x , food_y = self.foodPoint
            if (food_x - self.food_width//2 < current_x < (food_x + self.food_width//2) and
                    (food_y - self.food_width//2) < current_y < (food_y + self.food_width//2)):
                self.randomFoodLocation()
                self.allowedLength+=50
                self.score+=1

            # Draw Snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i!=0:
                        cv2.line(imgMain, self.points[i-1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 0), cv2.FILLED) #points[-1] returns the last point in the points list

            # Draw Food
            random_x, random_y = self.foodPoint
            # This function overlays a transparent PNG image (overlayImage) on top of another image (backgroundImage) at a specified position — and it does it cleanly, keeping the transparency intact (thanks to the alpha channel).
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (random_x - self.food_width//2, random_y - self.food_height//2))
            # Print Score
            cv2.putText(imgMain,f'Score = {self.score}' , (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 250, 50), thickness = 2 )

            # Check for Collission
            # Initially (example) , self.points = [(10, 20), (30, 40), (50, 60), (70, 80)]
            # Then self.points[:-2] would be: [(10, 20), (30, 40)]
            points = np.array(self.points[:-2],
                              np.int32)  # points[:-2] tells that take all points until the 2nd to last point
            # Now points looks like: array([[10, 20],
            #                               [30, 40]], dtype=int32)
            # Shape: (2, 2)
            points = points.reshape((-1, 1, 2))  # Reshaping the points array to make it compatible for the function
            #The position of -1 usually indicates the number of total points in the list,  -1 arugment tells numpy that - I don’t know how many points there will be — you figure it out automatically based on the original array’s size — but I want the second and third dimensions to be 1 and 2.”
            # This reshapes it to:
            #       array([[[10, 20]],
            #               [[30, 40]]], dtype=int32)
            # Shape: (2, 1, 2)
            cv2.polylines(imgMain, [points], False, (0, 200, 0), 3)
            minimumDistance = cv2.pointPolygonTest(points, (current_x, current_y),True ) # The last parameter (True) says the function that we want to measure the minimum distance between the set of points and the given point
            if -1 <= minimumDistance <= 1:
                self.gameOver = True
                self.points = []  # list of all points of the snake structure
                self.lengths = []  # distance between each point
                self.current_length = 0  # total length of the snake
                self.allowedLength = 200  # total allowed length This is the initial length of the snake, and the length will grow further after eating food
                self.previousHead = 0, 0  # coordinate of the previous head


        return imgMain

game = SnakeGameClass(pathFood)

while True:
    success, img = cap.read()
    img = cv2.flip(img, flipCode=1) # flipcode = 1 , we are flipping horizontally
    hands, img = detector.findHands(img, flipType = False)

    # We need the landmark point of the index finger.
    if hands:
        landmarkList = hands[0]['lmList'] #Since we have configured the findHands function to detect one hand only, so hands[0] gives the dictionary containing different data about the first hand and we want the landmarklist from that dictionary
        pointIndex = landmarkList[8][0:2]   # Point number 8 has the cooridnates for the fingertip we are interested about, and since we are dealing with a 2D plane, we'll ignore the z axis value
        #In the above list 2 is not inclusive, so we get the x, y coorodinates at 0 and 1 excluding the z coordinate at 2
        cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)
        img = game.update(img, pointIndex)

    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        game.gameOver = False
        game.score = 0
