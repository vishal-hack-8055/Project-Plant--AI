import imutils.contours
import cv2 
# from picamera.array import PiRGBArray
# from picamera import PiCamera
from time import sleep


args = 40
up_image=cv2.imread('images/height_test1.jpg')
image=cv2.resize(up_image,(400,900),interpolation=cv2.INTER_AREA)

# Convert to grayscale and blur
greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
greyscale = cv2.GaussianBlur(greyscale,(7,7),cv2.BORDER_DEFAULT)
# Detect edges and close gaps
canny_output = cv2.Canny(greyscale, 50, 100)
canny_output = cv2.dilate(canny_output, None, iterations=1)
canny_output = cv2.erode(canny_output, None, iterations=1)

# Get the contours of the shapes, sort l-to-r and create boxes
(contours, _ )= cv2.findContours(canny_output, cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)
if len(contours) < 2:
    print("Couldn't detect two or more objects")
    exit(0)

(contours, _) = imutils.contours.sort_contours(contours)
contours_poly = [None]*len(contours)
boundRect = [None]*len(contours)
for i, c in enumerate(contours):
    contours_poly[i] = cv2.approxPolyDP(c, 3, True)
    boundRect[i] = cv2.boundingRect(contours_poly[i])

output_image = image.copy()
mmPerPixel = args / boundRect[0][2]
highestRect = 1000
lowestRect = 0

for i in range(1, len(contours)):

    # Too smol?
    if boundRect[i][2] < 50 or boundRect[i][3] < 50:
        continue

    # The first rectangle is our control, so set the ratio
    if highestRect > boundRect[i][1]:
        highestRect = boundRect[i][1]
        
    if lowestRect < (boundRect[i][1] + boundRect[i][3]):
        lowestRect = (boundRect[i][1] + boundRect[i][3])

    # Create a boundary box
    cv2.rectangle(output_image, (int(boundRect[i][0]), int(boundRect[i][1])),
                  (int(boundRect[i][0] + boundRect[i][2]),
                  int(boundRect[i][1] + boundRect[i][3])), (255, 0, 0), 2)

# Calculate the size of our plant
plantHeight = (lowestRect - highestRect) * mmPerPixel
print("Plant height is {0:.0f}mm".format(plantHeight))

# Resize and display the image (press Esc key to exit)
resized_image = cv2.resize(output_image, (1280, 720))
cv2.imshow("Image", resized_image)
cv2.waitKey(0)