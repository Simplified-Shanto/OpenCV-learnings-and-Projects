import cv2
import mediapipe as mp
import time

# Press Ctrl+rightMousekey to access the definition of a function of a particular module
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose # Grabs the pose module from MediaPipe’s solutions package. Why? Because MediaPipe has many solutions like hands, face_mesh, holistic, etc. You're specifically calling the pose estimation module, which tracks 33 body landmarks.
pose = mpPose.Pose() #Initializes the pose estimation pipeline using default parameters. This creates a Pose object that can process images and return detected landmarks, confidence scores, etc.

cap = cv2.VideoCapture('testvideo2.mp4')
previousTime = 0

while True:
    success, img = cap.read() #image is in BGR format
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # mediapipe functions uses RGB image
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks,  mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape # h = height, w = width, c = channel
            #print("id = ", id, "lm = ", lm) #
            pixelX , pixelY = int(lm.x * w), int(lm.y * h) # lm.x and lm.y gives us the relative position of the landmark in the frame as a ratio, so we need to multiply that ratio with the widht and height of our frame to get the pixel position of the landmark
            cv2.circle(img, (pixelX, pixelY), 5, (255, 0, 0), cv2.FILLED) # The circle overlaps with the particular landmark, if we have the correct calculation for the landmark's position in pixel.

    currentTime = time.time()
    fps = 1/(currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break