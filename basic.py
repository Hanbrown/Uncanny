import cv2 as cv
import numpy as np

img = cv.imread("photos/tracks.JPG")

cv.imshow("Tracks", img)


grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow("Greyscale", grey)

# Blur
blur = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)
cv.imshow("Blur", blur)

# Edge Cascade (Canny)
canny = cv.Canny(blur, 100, 200)
cv.imshow("Canny Edges", canny)

lines = cv.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

for i in range(1, len(lines)):
    prev_line = lines[i-1]
    cur_line = lines[i]

    x1, y1, x2, y2 = prev_line[0]
    x3, y3, x4, y4 = cur_line[0]

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom != 0:
        px = ( (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4) ) / denom
        py = ( (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4) ) / denom

        cv.circle(img, (round(px), round(py)), radius=1, color=(255, 0, 0), thickness=5)


cv.imshow("Hough", img)



# dilated = cv.erode(canny, (3, 3), iterations=1)
# cv.imshow("Dilated", dilated[50:200, 200:400])

cv.waitKey(0)