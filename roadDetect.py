import cv2
import numpy as np
import math

class roadDetect:
    LX1 = 0
    LY1 = 1
    LX2 = 2
    LY2 = 3

    def __init__(self, val):
        self.isit = val

    @staticmethod
    def binarize(im, thresh):

        res = np.uint8(np.zeros(im.shape)) #[[0] * len(im[0,:]) for i in range(len(im[:,0]))]
        maxVal = 255
        minVal = 0
        for i in range(len(im[:,0])):
            for j in range(len(im[0,:])):
                if im[i,j] > thresh:
                    res[i,j] = maxVal
                else:
                    res[i,j] = minVal
        return res

    @staticmethod
    def region_of_interest(img, vertices):
        mask = np.zeros_like(img)
        # Used for if you're masking an rgb image
        # channel_count = img.shape[2]

        # used for anding our image with the mask
        match_mask_color = 255  # (255,) * channel_count #one is for grayscale, the other for color

        # Fill inside the polygon
        cv2.fillConvexPoly(mask, vertices, match_mask_color)

        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    @staticmethod
    # This function splits the image into slices and then runs houghlines on each slice. If you want to change the parameters
    # of houghlines you'll have to do it within this function.
    def split_detect(canny_im, resolution, x_beg, x_fin):
        dy = len(canny_im[:, 0]) // resolution
        lines_res = np.array([[[0, 0, 0, 0]]])
        for n in range(resolution):
            y_beg = n * dy
            y_end = n * dy + dy
            temp_im = roadDetect.region_of_interest(canny_im,
                                            np.array([[x_beg, y_beg], [x_beg, y_end], [x_fin, y_end], [x_fin, y_beg]]))
            temp_lin = cv2.HoughLinesP(temp_im, rho=6, theta=np.pi / 60, threshold=100, lines=np.array([]),
                                       minLineLength=10, maxLineGap=400)
            if temp_lin is not None:  # make sure you detected a line
                lines_res = np.concatenate((lines_res, temp_lin), axis=0)
        return lines_res[1:]

    @staticmethod
    def draw_lines(img, lines, color, thickness=6):
        # If there are no lines to draw, exit.
        if lines is None:
            return
        # Create a blank image that matches the original in size.
        line_img = np.zeros(
            (
                img.shape[0],
                img.shape[1],
                3
            ),
            dtype=np.uint8,
        )
        # Loop over all lines and draw them on the blank image.
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
        # Merge the image with the lines onto the original.
        img_copy = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
        # Return the modified image.
        return img_copy

    #takes in an image and returns canny. you will need to mask it once it's done.
    @staticmethod
    def getCanny(im):
        im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        bin_im = roadDetect.binarize(im_hsv[:,:,2], 200)
        im_canGr = cv2.Canny(bin_im,100,150)
        im_canHSV = cv2.Canny(im_hsv[:, :, 1], 100, 150)
        return np.add(im_canGr, im_canHSV)

    @staticmethod
    # This will return the slope as an angle with respect to the x axis. From 0 to 179.9999999 in degrees
    def get_slope(line):
        angle = math.degrees(math.atan2(line[0, roadDetect.LY2] - line[0, roadDetect.LY1], line[0, roadDetect.LX2] - line[0, roadDetect.LX1]))
        if angle < 0:
            return angle + 180
        elif angle == 180:
            return 0
        return angle

    @staticmethod
    def isGoodLine(line, toleranceDeg):
        lineAng = roadDetect.get_slope(line)
        if lineAng < 90:
            return lineAng < toleranceDeg
        return (180 - lineAng) < toleranceDeg

    @staticmethod
    def getGoodLines(lines, toleranceDeg):
        if lines is not None:
            resLines = []
            for i in range(len(lines)):
                if roadDetect.isGoodLine(lines[i], toleranceDeg):
                    resLines.append(lines[i])
            if len(resLines) > 0:
                return resLines
        return None

    @staticmethod
    def detectIntersection(im, toleranceDeg, prevLine, prevLineSearchTolerance):
        # detect around a slice created by prevLine
        if prevLine is not None:
            boxL = max(min(prevLine[roadDetect.LY1], prevLine[roadDetect.LY2]) - prevLineSearchTolerance, 0)
            boxU = min(max(prevLine[roadDetect.LY1], prevLine[roadDetect.LY2]) + prevLineSearchTolerance, len(im[:, 0]))
            verts = [[0, boxL], [0, boxU], [len(im[0, :, 0]), boxU], [len(im[0, :, 0]), boxL]]
            im_masked = roadDetect.region_of_interest(im, verts)
            lines = cv2.HoughLinesP(im_masked, rho=6, theta=np.pi / 60, threshold=300, lines=np.array([]),
                                    minLineLength=100,
                                    maxLineGap=400)
            resLines = roadDetect.getGoodLines(lines, toleranceDeg)
            if resLines is not None:
                return resLines

        # if we didn't find any qualifying lines above or if we don't have a prevline
        lines = cv2.HoughLinesP(im, rho=6, theta=np.pi / 60, threshold=300, lines=np.array([]), minLineLength=100,
                                maxLineGap=400)
        return roadDetect.getGoodLines(lines, toleranceDeg)