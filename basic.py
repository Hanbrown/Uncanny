import math

import cv2 as cv
import numpy as np

img = cv.imread("photos/bowling.jpg")

grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Blur
blur = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)

# Edge Cascade (Canny)
canny = cv.Canny(img, 100, 200)
cv.imshow("Canny Edges", canny)

lines = cv.HoughLinesP(canny, 1, np.pi/90, 100, minLineLength=100, maxLineGap=150)

slopes = []
TOLERANCE = 0.01
for i in range(len(lines)):
    cur_line = lines[i]

    x1, y1, x2, y2 = cur_line[0]

    m = float((y2 - y1) / (x2 - x1))

    if m in slopes:
        continue
    print(m)
    slopes.append(m)


    # denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # if denom != 0:
    #     px = ( (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4) ) / denom
    #     py = ( (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4) ) / denom
    #
    #     cv.circle(img, (round(px), round(py)), radius=1, color=(255, 0, 0), thickness=5)


for line in lines:
    x1, y1, x2, y2 = line[0]
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    color = GREEN

    hdist = math.sqrt((y2-y1)**2 + (x2 - x1)**2)
    ldist = abs(y2-y1)
    angle = math.acos(ldist / hdist)

    if angle > math.pi / 4:
        color = RED

    cv.line(img, (x1, y1), (x2, y2), color, 1)

cv.imshow("Hough", img)

cv.waitKey(0)