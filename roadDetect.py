import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

class road_image:
    LX1 = 0
    LY1 = 1
    LX2 = 2
    LY2 = 3

    def __init__(self, val):
        self.isit = val
    @staticmethod
    def make_coordinates( image, line_parameters, y_values):
        slope, intercept = line_parameters
        y1 = y_values[0]
        y2 = y_values[1]
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        x3 = (x2-x1)/2
        y3 = (y2-y1)/2
        if x1 < 0:
            x1 = 0
        if x2 < 0:
            x2 = 0
        if y1 < 0:
            y1 = 0
        if y2 < 0:
            y2 = 0
        if x1 > image.shape[0]:
            x1 = image.shape[0]
        if x2 > image.shape[0]:
            x2 = image.shape[0]
        if y1 > image.shape[1]:
            y1 = image.shape[1]
        if y2 > image.shape[1]:
            y2 = image.shape[1]
        return np.array([x1, y1, x2, y2])

    @staticmethod
    def display_lines(image, lines, RGB_val):
        line_image = np.zeros_like(image)
        if lines is not None:
            for x1, y1, x2, y2 in lines: 
                cv2.line(line_image, (x1, y1), (x2, y2), RGB_val, 5)
        return line_image

    @staticmethod
    def display_lines_3D(image, lines, RGB_val):
        line_image = np.zeros_like(image)
        if lines is not None:
            for c in range(lines.shape[0]):
                for x1, y1, x2, y2 in lines[c]:
                    x1 = int(round(x1))
                    y1 = int(round(y1))
                    x2 = int(round(x2))
                    y2 = int(round(y2))
                    cv2.line(line_image, (x1, y1), (x2, y2), RGB_val, 5)
        return line_image


    @staticmethod
    def average_slope_intercept(image, lines, y_values):
        # left_fit = []
        # for line in lines:
        #     x1, y1, x2, y2 = line.reshape(4)
            # parameters = np.polyfit((x1, x2), (y1, y2), 1)
            # slope = parameters[0]
            # if slope == float("inf"):
            #     print("Found infinity stones")
            #     slope = 50000
            # if slope == 0:
            #     print("Found infinity stones")
            #     slope = 1
            # intercept = parameters[1]

        # fit_average = np.average(right_fit, axis = 0)
        
        # average_line = road_image.make_coordinates(image, fit_average, y_values)
        if lines is None:
            # print("no lines found")
            average_line = [0,0,0,0]
        else:
            # print(lines)
            average_line = [np.average(lines[:,:,0]), np.average(lines[:,:,1]), np.average(lines[:,:,2]), np.average(lines[:,:,3])]

        # x1_middle = (int(round((left_line[0] + right_line[0])/2))) 
        # y1_middle = (int(round((left_line[1] + right_line[1])/2)))
        # x2_middle = (int(round((left_line[2] + right_line[2])/2)))
        # y2_middle = (int(round((left_line[3] + right_line[3])/2)))
        # if x1_middle > 640 or x1_middle < 0:
        #     x1_middle = 0
        # if y1_middle > 480 or y1_middle < 0:
        #     y1_middle = 0
        # if x2_middle > 640 or x2_middle < 0:
        #     x2_middle = 0
        # if y2_middle > 480 or y2_middle < 0:
        #     y2_middle = 0
        # center_line = np.array([x1_middle, y1_middle, x2_middle, y2_middle])
        # center_line = make_coordinates(image, center_fit_average)
        # cv2.line(image, (x1_middle, y1_middle), (x2_middle, y2_middle), (0, 255, 0), 10)
        return np.array([average_line])

    # This function splits the image into slices and then runs houghlines on each slice. If you want to change the parameters
    # of houghlines you'll have to do it within this function.
    @staticmethod
    def split_detect(canny_im_white_lines, canny_im_yellow_lines, resolution, x_beg, x_fin, original_image):
        dy = round(len(canny_im_white_lines[:,0])/resolution)
        right_line = np.array([[[0,0,0,0]]])
        left_line = np.array([[[0,0,0,0]]])
        for n in range(resolution,0,-1):
            y_beg = n*dy
            y_end = n*dy+dy
            temp_im_white_lines = road_image.image_slices(canny_im_white_lines, np.array([[x_beg,y_beg],[x_beg,y_end],[x_fin,y_end],[x_fin,y_beg]]))
            temp_im_yellow_lines = road_image.image_slices(canny_im_yellow_lines, np.array([[x_beg,y_beg],[x_beg,y_end],[x_fin,y_end],[x_fin,y_beg]]))

            temp_lin_white = cv2.HoughLinesP(temp_im_white_lines, rho=6, theta=np.pi / 60, threshold=100, lines=np.array([]), minLineLength=30, maxLineGap=10)
            temp_lin_yellow = cv2.HoughLinesP(temp_im_yellow_lines, rho=6, theta=np.pi / 60, threshold=100, lines=np.array([]), minLineLength=30, maxLineGap=10)
            y_values = [y_beg, y_end]
            if temp_lin_white is not None: # make sure you detected a line
                for line in temp_lin_white:
                    # print(line)
                    cv2.line(canny_im_white_lines, (line[0,0], line[0,1]), (line[0,2], line[0,3]), (255, 0, 0), 10)
                left_temp_line = (road_image.average_slope_intercept(canny_im_white_lines, temp_lin_white, y_values))
                # print(left_temp_line)
                left_line = np.concatenate((left_line, [left_temp_line]), axis = 0)
            if temp_lin_yellow is not None: # make sure you detected a line
                for line in temp_lin_yellow:
                    # print(line)
                    cv2.line(canny_im_yellow_lines, (line[0,0], line[0,1]), (line[0,2], line[0,3]), (255, 0, 0), 10)
                right_temp_line = (road_image.average_slope_intercept(canny_im_yellow_lines, temp_lin_yellow, y_values))
                # print(right_temp_line)
                right_line = np.concatenate((right_line, [right_temp_line]), axis = 0)

        return right_line[1:], left_line[1:]

    #creates a slice of the given image
    @staticmethod
    def image_slices(img, vertices):
        mask = np.zeros_like(img)
        #Used for if you're masking an rgb image
        #channel_count = img.shape[2]

        #used for anding our image with the mask
        match_mask_color = 255 #(255,) * channel_count #one is for grayscale, the other for color

        # Fill inside the polygon
        cv2.fillConvexPoly(mask, vertices, match_mask_color)

        # Returning the image only where mask pixels match
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    @staticmethod
    def binarize(im, thresh):
        conBlur = cv2.GaussianBlur(im, (5,5), 0)
        ret1, thresh1 = cv2.threshold(im,180,255,0)
        ret2, thresh2 = cv2.threshold(conBlur,180,255,0)
        conCombine = cv2.bitwise_or(thresh1,thresh2)
        return conCombine

    #takes in an image and returns canny. you will need to mask it once it's done.
    @staticmethod
    def getCanny(im):
        im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        bin_im = road_image.binarize(im_hsv[:,:,2], 200) #value = white lines
        im_canGr = cv2.Canny(bin_im,100,150) #good white lines image
        im_canHSV = cv2.Canny(im_hsv[:, :, 1], 100, 150) #hue = yellow lines, good yellow lines image
        im_white_lines = im_canGr
        im_yellow_lines = im_canHSV
        return im_white_lines, im_yellow_lines #np.add(im_canGr, im_canHSV)

    @staticmethod
    # This will return the slope as an angle with respect to the x axis. From 0 to 179.9999999 in degrees
    def get_slope(line):
        angle = math.degrees(math.atan2(line[0, road_image.LY2] - line[0, road_image.LY1], line[0, road_image.LX2] - line[0, road_image.LX1]))
        if angle < 0:
            return angle + 180
        elif angle == 180:
            return 0
        return angle

    @staticmethod
    def isGoodLine(line, toleranceDeg):
        lineAng = road_image.get_slope(line)
        if lineAng < 90:
            return lineAng < toleranceDeg
        return (180 - lineAng) < toleranceDeg

    @staticmethod
    def getGoodLines(lines, toleranceDeg):
        if lines is not None:
            resLines = []
            for i in range(len(lines)):
                if road_image.isGoodLine(lines[i], toleranceDeg):
                    resLines.append(lines[i])
            if len(resLines) > 0:
                return resLines
        return None

    @staticmethod
    def intersection_point(x1, x2, y1, y2):
        a = np.vstack([x1, x2, y1, y2])
        b = np.hstack((a, np.ones((4, 1))))
        line1 = np.cross(b[0], b[1])
        line2 = np.cross(b[2], b[3])
        x, y, z = np.cross(line1, line2)
        if z == 0:
            return (float('inf'), float('inf'))
        return (x/z, y/z)

    @staticmethod
    def region_of_interest(image, color):
        height = image.shape[0]
        width = image.shape[1]
        white = np.array([
            [(300, 460), (640, 460), (640, 190), (300, 190)]
        ])
        yellow = np.array([
            [(200, 460), (640-200, 460), (640-200, 190), (200, 190)]
        ])
        mask = np.zeros_like(image)
        if color == "WHITE":
            cv2.fillPoly(mask, white, 255)
        elif color == "YELLOW":
            cv2.fillPoly(mask, yellow, 255)
        else:
            return image
        masked_image = cv2.bitwise_and(image, mask) 
        return masked_image

    @staticmethod
    def detectIntersection(im, toleranceDeg, prevLine, prevLineSearchTolerance):
        # detect around a slice created by prevLine
        if prevLine is not None:
            boxL = max(min(prevLine[road_image.LY1], prevLine[road_image.LY2]) - prevLineSearchTolerance, 0)
            boxU = min(max(prevLine[road_image.LY1], prevLine[road_image.LY2]) + prevLineSearchTolerance, len(im[:, 0]))
            verts = [[0, boxL], [0, boxU], [len(im[0, :, 0]), boxU], [len(im[0, :, 0]), boxL]]
            im_masked = road_image.region_of_interest(im, verts, "WHITE")
            lines = cv2.HoughLinesP(im_masked, rho=6, theta=np.pi / 60, threshold=300, lines=np.array([]),
                                    minLineLength=50,
                                    maxLineGap=5)
            resLines = road_image.getGoodLines(lines, toleranceDeg)
            if resLines is not None:
                return resLines

        # if we didn't find any qualifying lines above or if we don't have a prevline
        lines = cv2.HoughLinesP(im, rho=6, theta=np.pi / 60, threshold=300, lines=np.array([]), minLineLength=100,
                                maxLineGap=400)
        return road_image.getGoodLines(lines, toleranceDeg)