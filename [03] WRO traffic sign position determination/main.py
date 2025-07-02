import cv2
import numpy as np
import imageStacker

# Object size and camera focal length (in cm and px)
KNOWN_WIDTH_CM = 10.0
ASPECT_RATIO = 2.0 # = Length of object / Width of object
FOCAL_LENGTH = 621.0

def detect_color(hsv, mask):
      # Red color range (two segments due to hue wrap-around)
    red_lower1 = np.array([0, 120, 70])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 120, 70])
    red_upper2 = np.array([180, 255, 255])

    # Blue color range
    blue_lower = np.array([100, 150, 50])
    blue_upper = np.array([140, 255, 255])

    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    red_mask = red_mask1 + red_mask2
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    red_overlap = cv2.bitwise_and(red_mask, red_mask, mask=mask)
    blue_overlap = cv2.bitwise_and(blue_mask, blue_mask, mask=mask)
    cv2.imshow("red_overlap", red_overlap)
    cv2.imshow("blue_overlap", blue_overlap)

    red_pixels = cv2.countNonZero(red_overlap)
    blue_pixels = cv2.countNonZero(blue_overlap)

    if red_pixels > blue_pixels and red_pixels > 100:
        return "Red"
    elif blue_pixels > red_pixels and blue_pixels > 100:
        return "Blue"
    else:
        return "Unknown"

def estimate_distance(perceived_width_px):
    if perceived_width_px == 0:
        return 0
    return round((KNOWN_WIDTH_CM*FOCAL_LENGTH)/perceived_width_px, 2)

def find_focal_length(actual_distance, perceived_width_px):
    return (actual_distance*perceived_width_px)/KNOWN_WIDTH_CM #cm
    
def empty():
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Threshold1", "TrackBars", 0, 255, empty) # first numerical argument indicates the initial value of the trackbar, and the later one is the range of the trackbar
cv2.createTrackbar("Threshold2", "TrackBars", 20, 255, empty)
cv2.createTrackbar("Kernel", "TrackBars", 5, 30, empty)
cv2.createTrackbar("SigmaX", "TrackBars", 0, 20,  empty)
#Canny Thresholds must be 0 ≤ threshold1 < threshold2 ≤ 255 (since image pixel values are in 8-bit format)



# --- Define HSV ranges for Red and Blue (Need tuning!) ---
# Red color mask 
RED_LOWER_1 = np.array([0, 120, 70])
RED_UPPER_1 = np.array([10, 255, 255])
RED_LOWER_2 = np.array([170, 120, 70])
RED_UPPER_2 = np.array([180, 255, 255])

# Blue color range 
BLUE_LOWER = np.array([100, 150, 50])
BLUE_UPPER = np.array([140, 255, 255])

# cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
# cv2.createTrackbar("Sat Min", "TrackBars", 110, 255, empty)
# cv2.createTrackbar("Value Min", "TrackBars", 153, 255, empty)
# cv2.createTrackbar("Hue Max", "TrackBars", 19, 179, empty)
# cv2.createTrackbar("Sat Max", "TrackBars", 240, 255, empty)
# cv2.createTrackbar("Value Max", "TrackBars", 255, 255, empty)


def main():
    cap = cv2.VideoCapture(2)
    while True:
        success, frame = cap.read()
        #success = true when the webcam successfully captures a frame
        # success = false - When something goes wrong: 1. Webcam is not connected 2. It’s being used by another program 3. End of a video file (if reading from video) 4. Permissions issue (e.g., camera blocked)
        if success == False: 
            break
        detection_frame = frame.copy()
        imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blue_mask = cv2.inRange(imgHsv, BLUE_LOWER, BLUE_UPPER)
        masked_frame = cv2.bitwise_and(frame, frame, mask = blue_mask)


    #     red_count = 0
    #     blue_count = 0
    #     red_distances = []
    #     blue_distances = []

    #     red_axis = {"X":0, "Y":0}  #Python dictionary
    #     blue_axis = {"X":0, "Y":0}

    #     #to smooth out noise before edge detection.
    #     kernel = cv2.getTrackbarPos("Kernel", "TrackBars")
    #     if kernel%2==0: kernel = kernel+1
    #     sigmaX = cv2.getTrackbarPos("SigmaX", "TrackBars")
    #     imgBlurred = cv2.GaussianBlur(frame, (kernel, kernel), sigmaX) # cv2.GaussianBlur(src, ksize, sigmaX) 
    #     #ksize = Kernel size (width, height) — must be odd (e.g., (3,3), (5,5), etc.), Larger kernel (e.g., (7,7), (11,11)) → more blur, smoother image, Smaller kernel (e.g., (3,3)) → less blur, more details preserved
    #     #More blur means - less noise, smoother edges, fewer false edges BUT over-blurring may erase small or weak edges (important if you're detecting shapes or small boxes)
    #     #So it's trade-off: Too little blur = noisy edges, too much blur = missed details
    #     imgGray = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)

    #     lowThreshold = cv2.getTrackbarPos("Threshold1", "TrackBars")
    #     highThreshold = cv2.getTrackbarPos("Threshold2", "TrackBars")
    #     imgCanny = cv2.Canny(imgGray,lowThreshold , highThreshold) # Last two parameters - first one = lower threshold, second one = upper threshold, these control how edges are detected

        contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        roi_mask = np.zeros(frame.shape, dtype=np.uint8) #imgGray.shape → (height, width):This returns a tuple representing the dimensions of the grayscale image.
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02*cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)

            if len(approx) == 4 and area > 1000:
                x, y, w, h = cv2.boundingRect(approx)
                rect_aspect = max(w, h) / min(w, h)
                print("Rectangle found!")
                # if not (1.6 <= rect_aspect <=2.4):
                #      print("Aspect ratio mismatch")
                #      continue
                roi_mask = np.zeros(frame.shape, dtype=np.uint8) 
                cv2.drawContours(roi_mask, [approx], -1, 255, -1) # last 3 arguments are 1. contourIndex, 2. color , 3. thickness
                #contourIndex - tells openCV which contour to draw; -1 means draw all contours in the list, Since you're only passing [approx], it's just one — so -1 = draw that one.
                #thickness - This controls how thick the drawn line should be.-1 means: fill the entire shape (i.e., a filled-in polygon). If you used, say, 2, you'd just get an outline — not useful for masking.
                cv2.imshow("roi_mask", roi_mask)
                # color = detect_color(imgHsv, roi_mask)
                # print("Color = ", color)
                distance_cm = estimate_distance(max(w,h))
                print("Distance = ", distance_cm)
    #             center_x = x + w//2 # / performs true division - always returning a floating point number
    #             center_y = y + h//2 # // performs floor division - quotient is rounded down to the nearest whole number
            
    #             if color == "Red":
    #                 red_count+=1
    #                 red_distances.append(distance_cm)
    #                 if red_count == 1:
    #                     red_axis = {"X":center_x, "Y":center_y}
    #             elif color == "Blue":
    #                 blue_count+=1
    #                 blue_distances.append(distance_cm)
    #                 if blue_count == 1:
    #                     blue_axis = {"X": center_x, "Y": center_y}
                
    #             cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
    #             cv2.putText(frame, f'{color} {distance_cm}cm', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (2555, 255, 255), 2)
                    
        
        
                
        
        
        imgStack = imageStacker.stackImages(0.5, ([frame, imgHsv], [blue_mask, masked_frame]))
        cv2.imshow("Stacked Images", imgStack)


        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            
            break
        #cv2.waitKey(1) waits for a key event for 1 millisecond. 
        #If no key is pressed during this time, it returns -1. If a key is pressed, it returns a 32-bit integer (platform-dependent) which contains information about the key.
        #Doing a bitwise AND & 0xFF extracts the last 8 bits of the returned integer — i.e., the actual ASCII key value (like 'q' → 113).
        #ord('q') returns the ascii value of 'q' which is 113. 
        #The function ord() in Python stands for "ordinal", which refers to the numeric position of a character in the Unicode (or ASCII) table.q
if __name__ == "__main__":
    main()