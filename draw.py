import cv2 as cv
import numpy as np

img = cv.imread("photos/plane.JPG")

blank = np.zeros((600, 700, 3), dtype = "uint8")

# cv.imshow("blank", blank)

# 1. Paint image a certain color
blank[:] = 255, 255, 255
# cv.imshow("Green", blank)

cv.rectangle(blank, (0, 0), (blank.shape[1], blank.shape[0]//3), (20, 89, 194), thickness=-1)
cv.rectangle(blank, (0, blank.shape[0]*2//3), (blank.shape[1], blank.shape[0]), (57, 174, 99), thickness=-1)

cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), blank.shape[0]//6 - 10, (20, 89, 194), thickness=-1)

cv.putText(blank, "Republique du Niger", (175, 225), cv.FONT_HERSHEY_TRIPLEX, 1.0, (75, 75, 75), 2)

cv.imshow("Niger", blank)
cv.waitKey(0)

# 30:00, https://www.youtube.com/watch?v=oXlwWbU8l2o