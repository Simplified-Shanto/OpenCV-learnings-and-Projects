import cv2
import mediapipe as mp
import time
# Press Ctrl+rightMousekey to access the definition of a function of a particular module

# We'll have all these functionalities and features inside a class for maximum reusability of this code piece in the future.
class poseDetector():
    def __init__(self, mode = False, upperBody = False, smooth = True,
                 detectionConf = 0.5, trackingConf = 0.5):
        self.mode = mode
        self.upperBody = upperBody
        self.smooth = smooth
        self.detectionCon = detectionConf #detection confidence
        self.trackingCon  = trackingConf  #tracking confidence

        self.mpDraw = mp.solutions.drawing_utils # Grabs the pose module from MediaPipe’s solutions package. Why? Because MediaPipe has many solutions like hands, face_mesh, holistic, etc. You're specifically calling the pose estimation module, which tracks 33 body landmarks.
        self.mpPose = mp.solutions.pose          #Initializes the pose estimation pipeline using default parameters. This creates a Pose object that can process images and return detected landmarks, confidence scores, etc.

        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=1,
            smooth_landmarks=self.smooth,
            enable_segmentation=False,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackingCon
        )

    def findPose(self, img, draw = True): #Draw is a flag which asks a user whether he wants to draw the landmarks on the image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # mediapipe functions uses RGB image
        self.results =   self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img, draw = True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape # h = height, w = width, c = channel
                #print("id = ", id, "lm = ", lm) #
                pixelX , pixelY = int(lm.x * w), int(lm.y * h) # lm.x and lm.y gives us the relative position of the landmark in the frame as a ratio, so we need to multiply that ratio with the widht and height of our frame to get the pixel position of the landmark
                lmList.append([id, pixelX, pixelY])
                if draw:
                    cv2.circle(img, (pixelX, pixelY), 5, (255, 0, 0), cv2.FILLED) # The circle overlaps with the particular landmark, if we have the correct calculation for the landmark's position in pixel.

        return lmList

def main():
    cap = cv2.VideoCapture('testvideo1.mp4')
    previousTime = 0
    detector = poseDetector()

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


if __name__== "__main__":
    main()

#Every Python file has a special built-in variable called __name__.
# If you're running this particular python code, then __name__ is automatically
# set to "__main__", but if you're importing this file into another python
# script like "import poseModule", then __name__ becomes "poseModule" and the
# main() functiona won't run automatically. This lets you separate reusable code
# from executable code.