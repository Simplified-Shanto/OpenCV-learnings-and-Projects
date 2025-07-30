import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize webcam
cap = cv2.VideoCapture(0)  # Change to 1 if you have an external webcam

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()

    # Find the hands and get info
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]  # Get first detected hand
        fingers = detector.fingersUp(hand)
        totalFingers = fingers.count(1)  # Count fingers that are up

        # Display count on screen
        cv2.putText(img, f'Fingers: {totalFingers}', (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

    # Show image
    cv2.imshow("Finger Counter", img)

    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
