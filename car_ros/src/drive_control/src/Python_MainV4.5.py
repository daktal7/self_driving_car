#!/usr/bin/env python
#Python_MainV2
# Python Main
import roadDetectV4
from roadDetectV4 import road_image as RI
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import serial
from signal import signal, SIGINT
import rospy
from std_msgs.msg import Float32
# import intersectionLaneSwitches as ils
# import wpManager as wpm
# import requests
import time
import imutils

writer = None
(W, H) = (None, None)


print("Test 1")

#############Serial Stuff Setup#############
ser = serial.Serial("/dev/ttyUSB0",115200)
print("1")
ser.flushInput()
print("2")
time.sleep(2)
print("3")
init_command = "!start1615\n"
print("4")
ser.write(init_command.encode())
print("5")
init_command = "!inits0.0002\n"
print("6")
ser.write(init_command.encode())
print("7")
init_command = "!kp0.01\n"
print("8")
ser.write(init_command.encode())
print("9")
init_command = "!kd0.01\n"
print("10")
ser.write(init_command.encode())
print("11")
init_command = "!pid0\n"
print("12")
ser.write(init_command.encode())
print("13")


print("test1.5")

def speed(value):
    command="!speed" + str(value) + "\n"
    ser.write(command.encode())

def steer(value):
	value = int(value)
	if value != steer.prevAngle:
		prevAngle = value
		command="!steering" + str(value) + "\n"
		ser.write(command.encode())
	
# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    writer.release()
    cap.release()
    print('CTRL-C detected. Exiting gracefully')
    exit(0)

steer.prevAngle = 0

print("test2")

signal(SIGINT, handler)
print('Running. Press CTRL-C to exit')

#the function (copied from Learning Suite) to get you location 
def getCoor(color):
    # api-endpoint
    URL = "http://192.168.1.8:8080/%s" % color
 
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
 
    # extracting data
    coorString = r.text
    coordinates = coorString.split()
    latitude = float(coordinates[0])
    longitude = float(coordinates[1])
    return (latitude, longitude)

def turn_left_through_intersection():
    steer(-25)
    time.sleep(1.5)

def turn_right_through_intersection():
    steer(25)
    time.sleep(1.5)

def straight_through_intersection():
    steer(0)
    time.sleep(1.5)


FRAMES_TO_AVERAGE = 1
DRIVING_SPEED = 0.0002

number_of_slices = 5
dynamic_coordinates_right = [[[123,123],[123,123],[123,123],[123,123]]]
dynamic_coordinates_left = [[[123,123],[123,123],[123,123],[123,123]]]
for num in range(number_of_slices):
    dynamic_coordinates_right = np.concatenate((dynamic_coordinates_right, [[[123,123],[123,123],[123,123],[123,123]]]), axis = 0)
    dynamic_coordinates_left = np.concatenate((dynamic_coordinates_left, [[[123,123],[123,123],[123,123],[123,123]]]), axis = 0)

# start of the Main
# yellow_pic
# frame = cv2.imread('color_wheel.png')
cap = cv2.VideoCapture("/dev/video2",cv2.CAP_V4L)
# cap = cv2.VideoCapture("roadTest2.avi")
#cap = cv2.VideoCapture("MOVIE_2.avi")

#pub = rospy.Publisher('steerAngle', Float32, queue_size=10)
#rospy.init_node('angleTalker', anonymous=False)
#rate = rospy.Rate(10)

turnIndex=0

# print("Test3")
steering_angle = 0
time.sleep(5)
speed(DRIVING_SPEED)
while(cap.isOpened()):
	steering_angle = 0
	for x in range(0,FRAMES_TO_AVERAGE):
		grabbed, frame = cap.read()
		if frame is None:
		    break
		# if the frame was not grabbed, then we have reached the end
		# of the stream
		if not grabbed:
		    break

		image = cv2.resize(frame, (640, 480))

		lane_image = np.copy(image)
		canny_white_lines, canny_yellow_lines = RI.getCanny(lane_image)
		right_line, left_line, dynamic_roi_right = RI.split_detect(canny_white_lines, canny_yellow_lines, number_of_slices, 0, canny_white_lines.shape[1], lane_image,  dynamic_coordinates_left, dynamic_coordinates_right)
		if right_line.shape[0] != 0:
			line_image_right = RI.display_lines_3D(lane_image, right_line, (0,0,255))
		else:
			line_image_right = lane_image
		if left_line.shape[0] != 0:
			line_image_left = RI.display_lines_3D(lane_image, left_line, (0,255, 0))
		else:
			line_image_left = lane_image
		lines_to_average_right = right_line
		lines_to_average_right = np.array(lines_to_average_right)
		lines_to_average_left = left_line
		lines_to_average_left = np.array(lines_to_average_left)
		left_offset = 250
		right_offset = -150
		offset = 0
		# if left_line.shape[0] != 0 and right_line.shape[0] != 0: #this means I have a left and right line
		# 	average_line_left = [np.average(lines_to_average_left[:,:,0]), np.average(lines_to_average_left[:,:,1]), np.average(lines_to_average_left[:,:,2]), np.average(lines_to_average_left[:,:,3])]
		# 	average_line_right = [np.average(lines_to_average_right[:,:,0]), np.average(lines_to_average_right[:,:,1]), np.average(lines_to_average_right[:,:,2]), np.average(lines_to_average_right[:,:,3])]
		# 	if average_line_right[0] < average_line_left[0] or average_line_right[2] < average_line_left[2] or average_line_right[1] < average_line_left[2] or average_line_right[2] < average_line_left[1]:
		# 		steering_point = [int(average_line_left[2] + left_offset), int(average_line_left[3])]
		# 	else:
		# 		both_lines_to_average = [[average_line_left]]
		# 		both_lines_to_average = np.concatenate((both_lines_to_average, [[average_line_right]]), axis = 0)

		# 		average_line = [np.average(both_lines_to_average[:,:,0]), np.average(both_lines_to_average[:,:,1]), np.average(both_lines_to_average[:,:,2]), np.average(both_lines_to_average[:,:,3])]
		# 		if left_line.shape[0] > right_line.shape[0]: # more left lines so adjust it to the right a little
		# 			offset = 0
		# 		elif left_line.shape[0] < right_line.shape[0]: # more RIGHT lines so adjust it to the LEFT a little
		# 			offset = 0
		# 		steering_point = [int(average_line[2] + offset), int(average_line[3])]
		if left_line.shape[0] != 0:# and right_line.shape[0] == 0: # I only have the left line
			average_line = [np.average(lines_to_average_left[:,:,0]), np.average(lines_to_average_left[:,:,1]), np.average(lines_to_average_left[:,:,2]), np.average(lines_to_average_left[:,:,3])]
			steering_point = [int(average_line[2] + left_offset), int(average_line[3])]

		elif left_line.shape[0] == 0 and right_line.shape[0] != 0: # I only have the right line
			average_line = [np.average(lines_to_average_right[:,:,0]), np.average(lines_to_average_right[:,:,1]), np.average(lines_to_average_right[:,:,2]), np.average(lines_to_average_right[:,:,3])]
			steering_point = [int(average_line[2] + right_offset), int(average_line[3])]
			
		else: #this is a defualt value
			steering_point = (420,300)

		fudge_factor = 50
		if steering_point[0] > lane_image.shape[1] + fudge_factor:
			steering_point[0] = lane_image.shape[1] + fudge_factor
		if steering_point[1] > lane_image.shape[0] + fudge_factor:
			steering_point[1] = lane_image.shape[0] + fudge_factor
		steering_angle = steering_angle + RI.getDriveAngle(steering_point)
		# Check for intersection
		toleranceDeg = 5
		prevLine = None
		prevLineSearchTolerance = 20
		# closest_line_found = RI.detectIntersection(canny_white_lines, toleranceDeg, prevLine, prevLineSearchTolerance)
		intersection_theshold = 410
		turnIndex = turnIndex+1
		if turnIndex > 3:
			turnIndex = 0
					
		cv2.circle(lane_image, (steering_point[0], steering_point[1]), 10, (255,255,255), -1) #the color is organized as (blue, green, red)
		combo_image_lines = cv2.addWeighted(line_image_left, 0.5, line_image_right, 0.5, 1)
		combo_image = cv2.addWeighted(lane_image, 0.3, combo_image_lines, 1, 1)

		# if W is None or H is None:
		#     (H, W) = frame.shape[:2]

		# check if the video writer is None
		if writer is None:
		    # initialize our video writer
		    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		    writer = cv2.VideoWriter("./Zach_Wes_test.avi", fourcc, 30,
		        (640, 480), True)

		# write the output frame to disk
		# dynamic_roi_right = cv2.cvtColor(dynamic_roi_right, cv2.COLOR_GRAY2RGB)
		# dynamic_roi_right_resized = cv2.resize(dynamic_roi_right, (640, 480))
		writer.write(combo_image)

			
	steering_angle = steering_angle / FRAMES_TO_AVERAGE
	toleranceDeg = 5
	prevLine = None
	prevLineSearchTolerance = 20
	steer(steering_angle)
	#pub.publish(steering_angle)
	#rate.sleep()

