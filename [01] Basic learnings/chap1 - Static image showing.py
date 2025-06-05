import cv2
import numpy as np

img = cv2.imread("D:/[01] All types of photos/To be deleted temporary photos/pexels-photo-7456959.webp")
print(img.shape)

imgResize = cv2.resize(img, (400, 300))

imgCropped = img[200:333, 200:500]

cv2.imshow("Original", img)
cv2.imshow("Resized", imgResize)
cv2.imshow("cropped image", imgCropped)

cv2.waitKey(0)