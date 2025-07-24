import cv2
import pytesseract #PyTesseract is a Python library that acts as a wrapper for Google's Tesseract Optical Character Recognition (OCR) engine. It provides a user-friendly interface to leverage Tesseract's capabilities directly within Python applications.
                   #It allows developers to integrate powerful OCR functionalities into their Python projects, enabling tasks like automated data entry, document digitization, and text recognition from visual media.
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('sampletext.jpg')
img = cv2.imread('sampletext2.png')

#Pyetesseract only accepts RGB value
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#print(pytesseract.image_to_string(img))


## Detecting characters

# imgHeight, imgWidth,_ = img.shape
# Passing the configuration in in image_to_boxes for only digits will lead to detection of the digits only
# boxes = pytesseract.image_to_boxes((img)) #Returns the coordinates of the diagonal points
#
# for b in boxes.splitlines():
#     print(b)
#     b = b.split(' ') #b.split(' ') = splits on single spaces only # b.split() = splits on any whitespace (recommended in most cases)
#     #print(b)
#     x1,y1,x2,y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4]) #b[index] is of type string b[0] = detected character
#     # parameters of cv2.rectangle(image, pt1, pt2, color, thickness) pt1 = (x1, y1) → One corner (usually top-left) pt2 = (x2, y2) → The opposite corner (usually bottom-right)
#     cv2.rectangle(img, (x1,imgHeight-y1), (x2, imgHeight - y2), (0, 0, 255), 2) # OpenCV uses y=0 at the top, but the box coordinates use y=0 at the bottom, so we convert them using imgHeight - y
#     cv2.putText(img, b[0], (x1, imgHeight - y1 +30), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
#
# cv2.imshow("Result", img)
# cv2.waitKey(0)


### Detecting Words

# imgHeight, imgWidth,_ = img.shape
# boxes = pytesseract.image_to_data((img)) #Returns the coordinates of the diagonal points
# #print(boxes)
# for x, b in enumerate(boxes.splitlines()): # enumerate() returns (index, element) pairs as you iterate
#     print('x = ', x)                       # x = index of the item, b = the item itself.
#     if x!=0: # The first row in the list is the headings of the data columns, so we don't wont to detect anything there.
#         b = b.split() # b.split() let's tesseract decide what to use as a delimeter for words
#         print(b)
#         if len(b)==12: #both delimeters and words are present in the list, for a delimeter number of columns in b = 11, and for a word number of columns in b = 12
#             x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9]) # The 6th, 7th, 8th and 9th column in b represents x1, y1, x2, y2 of the bounding box
#             cv2.rectangle(img, (x , y),(x+w,y+h) , (0, 0, 255), 2 ) #Unlike pytesseract.image_to_boxes() image_to_data() returns bounding rectangle coordinate and dimension data in a format compatible with opencv coordinate notaiton
#             cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2  )
# cv2.imshow("Result", img)
# cv2.waitKey(0)

### Detecting digits only
imgHeight, imgWidth,_ = img.shape
configurations = r'--oem 3 --psm 6 outputbase digits' # Configuration for only detecting digits. OEM - refers to the engine mode
boxes = pytesseract.image_to_data(img, config = configurations) #Returns the coordinates of the diagonal points
#print(boxes)
for x, b in enumerate(boxes.splitlines()): # enumerate() returns (index, element) pairs as you iterate
    print('x = ', x)                       # x = index of the item, b = the item itself.
    if x!=0: # The first row in the list is the headings of the data columns, so we don't wont to detect anything there.
        b = b.split() # b.split() let's tesseract decide what to use as a delimeter for words
        print(b)
        if len(b)==12: #both delimeters and words are present in the list, for a delimeter number of columns in b = 11, and for a word number of columns in b = 12
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9]) # The 6th, 7th, 8th and 9th column in b represents x1, y1, x2, y2 of the bounding box
            cv2.rectangle(img, (x , y),(x+w,y+h) , (0, 0, 255), 2 ) #Unlike pytesseract.image_to_boxes() image_to_data() returns bounding rectangle coordinate and dimension data in a format compatible with opencv coordinate notaiton
            cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2  )
cv2.imshow("Result", img)
cv2.waitKey(0)