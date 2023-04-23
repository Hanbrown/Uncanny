import math

import cv2 as cv
import numpy as np

# Inefficient way to find intersections between all the lines. There must be a faster way to do this
def get_intersections(lines):
    points = []
    # Iterate through all the lines to find intersections
    for i in range(len(lines)):
        for j in range(i, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]

            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if denom != 0:
                px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
                py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

                points.append((round(px), round(py)))

    return points


def main():
    img = cv.imread("photos/bowling.jpg")

    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Blur
    # blur = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)

    # Edge Cascade (Canny)
    canny = cv.Canny(img, 100, 200)
    cv.imshow("Canny Edges", canny)

    lines = cv.HoughLinesP(canny, 1, np.pi / 90, 100, minLineLength=100, maxLineGap=150)

    # Add
    # slopes = []
    # for i in range(len(lines)):
    #     cur_line = lines[i]
    #
    #     x1, y1, x2, y2 = cur_line[0]
    #
    #     m = float((y2 - y1) / (x2 - x1))
    #
    #     if m in slopes:
    #         continue
    #     slopes.append(m)

    heights = []
    grounds = []

    # Find which lines are truly vertical and which lines are truly horizontal
    for line in lines:
        x1, y1, x2, y2 = line[0]
        RED = (0, 0, 255)
        GREEN = (0, 255, 0)

        color = GREEN

        hdist = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        ldist = abs(y2 - y1)
        angle = math.acos(ldist / hdist)

        # Use tolerance angles to make sure lines correspond to perpendicular surfaces.
        # This method should be improved. It will not work on all images
        if angle > 7*math.pi / 16:
            color = RED
            grounds.append(line)
        elif angle < 3*math.pi / 8:
            heights.append(line)
        else:
            continue

        cv.line(img, (x1, y1), (x2, y2), color, 1)

    # m -> median; h -> height
    points = get_intersections(heights)
    arr = np.array(points)
    mhy = int(np.median(arr[:, 1].astype(float)))
    mhx = int(np.median(arr[:, 0].astype(float)))
    v1 = (mhx, mhy)

    # m -> median; g -> ground
    points = get_intersections(grounds)
    arr = np.array(points)
    mgy = int(np.median(arr[:, 1].astype(float)))
    mgx = int(np.median(arr[:, 0].astype(float)))
    v2 = (mgx, mgy)

    cv.circle(img, (mhx, mhy), radius = 1, color = (255, 0, 255), thickness=5)

    cv.imshow("Hough", img)

    # Arbitrary point and the center of the image
    x1 = int(img.shape[1] / 2)
    x2 = 167
    y1 = int(img.shape[0] / 2)
    y2 = 180

    c = (x1, y1)

    # Find projection of image center on intersection line (Vi in the paper)
    x3 = mhx
    x4 = mgx
    y3 = mhy
    y4 = mgy
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom != 0:
        vix = ( (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4) ) / denom
        viy = ( (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4) ) / denom
        vi = (round(vix), round(viy))


    cv.circle(img, vi, radius = 1, color = (255, 0, 255), thickness=5)
    cv.circle(img, c, radius = 1, color = (255, 0, 255), thickness=5)

    cv.imshow("Hough", img)

    viv2 = math.dist(vi, v2) / 332 * 100
    v1vi = math.dist(v1, vi) / 332 * 100
    oivi = math.dist(c, vi) / 332 * 100

    ocvi = math.sqrt(v1vi * viv2)
    f = math.sqrt((ocvi**2) - (oivi**2))

    print(f)

    # Calculate Rotation Matrix
    ## First, find x, y, and z vectors
    oc = (0, 0)
    ocv1 = math.dist(oc, v1) / 332 * 100
    ocv2 = math.dist(oc, v2) / 332 * 100

    xc = [v1[0] / ocv1, v1[1] / ocv1, f / ocv1]
    yc = [v2[0] / ocv2, v2[1] / ocv2, f / ocv2]
    zc = np.cross(xc, yc)

    # Now find R
    denom1 = math.sqrt(v1[0]**2 + v1[1]**2 + f)
    denom2 = math.sqrt(v2[0]**2 + v2[1]**2 + f)

    R1 = [v1[0] / denom1, v2[0] / denom2, zc[0]]
    R2 = [v1[1] / denom1, v2[1] / denom2, zc[1]]
    R3 = [f / denom1, f / denom2, zc[2]]

    R = [R1, R2, R3]

    print(R)

    # Apply R to a 2x2x2 cube
    pt = [[1], [1], [1]]
    print(np.matmul(R, pt))

    pt = [[1], [1], [-1]]
    print(np.matmul(R, pt))

    pt = [[1], [-1], [1]]
    print(np.matmul(R, pt))

    pt = [[1], [-1], [-1]]
    print(np.matmul(R, pt))

    pt = [[-1], [1], [1]]
    print(np.matmul(R, pt))

    pt = [[-1], [1], [-1]]
    print(np.matmul(R, pt))

    pt = [[-1], [-1], [1]]
    print(np.matmul(R, pt))

    pt = [[-1], [-1], [-1]]
    print(np.matmul(R, pt))

    cv.waitKey(0)


main()
