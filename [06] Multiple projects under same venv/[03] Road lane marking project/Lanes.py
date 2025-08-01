import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def returnCanny(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)
    imgCanny = cv2.Canny(imgBlur, 50, 150)
    return imgCanny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([(200, height), (1100, height), (550, 250)], np.int32) # The returned numpy array contains the 3 vertex coordinate of the triangular region of interest which is compatible to be passed to the fillPoly function. The fillPoly function expects the array members to be of int32 type
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [triangle], (255, 255, 255) )
    img_masked = cv2.bitwise_and(image, mask)
    return img_masked




# image = cv2.imread('test_image.jpg') #Loads image having BGR colorspace
# lane_image = np.copy(image) # doing lane_image = image changes the original image when we change lane_image
# imgCanny = returnCanny(lane_image)
# cropped_image = region_of_interest(imgCanny)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap = 5)
#
# averaged_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# final_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# cv2.imshow("ROI", final_image) # The imshow method of matplotlib doesn't require a window name to execute
# cv2.waitKey(0)


cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    #image = cv2.imread('test_image.jpg')  # Loads image having BGR colorspace
    lane_image = np.copy(frame)  # doing lane_image = image changes the original image when we change lane_image
    imgCanny = returnCanny(lane_image)
    cropped_image = region_of_interest(imgCanny)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)

    averaged_lines = average_slope_intercept(lane_image, lines)
    line_image = display_lines(lane_image, averaged_lines)
    final_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    cv2.imshow("ROI", final_image)  # The imshow method of matplotlib doesn't require a window name to execute
    key = cv2.waitKey(1)
    if key == ord('q'):
        break