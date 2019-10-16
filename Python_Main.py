# Python Main
import roadDetect
from roadDetect import road_image as RI
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

# start of the Main

# image = cv2.imread('7.jpg')
cap = cv2.VideoCapture("road_test4.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    if frame is None:
        break
    image = cv2.resize(frame, (640, 480))

    lane_image = np.copy(image)
    canny_white_lines, canny_yellow_lines = RI.getCanny(lane_image)
    cropped_image_white_lines = RI.region_of_interest(canny_white_lines, "WHITE")
    cropped_image_yellow_lines = RI.region_of_interest(canny_yellow_lines, "YELLOW")
    number_of_slices = 5
    right_line, left_line = RI.split_detect(cropped_image_white_lines, cropped_image_yellow_lines, number_of_slices, 0, cropped_image_white_lines.shape[1], lane_image)
    # print(s_lines)
    # print(right_line.shape)
    if right_line.shape[0] != 0:
    	line_image_right = RI.display_lines_3D(lane_image, left_line, (255,0,0))
    else:
    	line_image_right = lane_image
    if left_line.shape[0] != 0:
    	line_image_left = RI.display_lines_3D(lane_image, right_line, (0,255, 0))
    else:
    	line_image_left = lane_image
        # print(right_line)
        # print(left_line)
    combo_image_lines = cv2.addWeighted(line_image_left, 1, line_image_right, 1, 1)
    # lane_image = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    combo_image = cv2.addWeighted(lane_image, 0.5, combo_image_lines, 1, 1)


        # a1 = averaged_lines[0][0], averaged_lines[0][1]
        # a2 = averaged_lines[0][2], averaged_lines[0][3]
        # b1 = averaged_lines[1][0], averaged_lines[1][1]
        # b2 = averaged_lines[1][2], averaged_lines[1][3]
        # vanishing_point = RI.intersection_point(a1, a2, b1, b2)
        # vanishing_point = (int(round(vanishing_point[0])), int(round(vanishing_point[1])))
        # cv2.circle(combo_image, vanishing_point, 5, (0,0, 255), 4)

        # combo_image = cropped_image_white_lines
    # else:
    # 	print("failed?")
    # 	combo_image = cropped_image_white_lines
    


    # plt.imshow(combo_image)
    # plt.show()
    cv2.imshow("result", combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break




