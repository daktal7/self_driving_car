#!/usr/bin/env python
#Python_MainV2
# Python Main
import roadDetectV4
from roadDetectV2 import road_image as RI
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


print("Test 1")

#############Serial Stuff Setup#############
ser = serial.Serial("/dev/ttyUSB0",115200)
print("1")
ser.flushInput()
print("2")
time.sleep(2)
print("3")
init_command = "!start1750\n"
print("4")
ser.write(init_command.encode())
print("5")
init_command = "!inits1.5\n"
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


FRAMES_TO_AVERAGE = 5
DRIVING_SPEED = 0.5

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
		_, frame = cap.read()
		if frame is None:
		    break

		image = cv2.resize(frame, (640, 480))

		lane_image = np.copy(image)
		canny_white_lines, canny_yellow_lines = RI.getCanny(lane_image)
		right_line, left_line = RI.split_detect(canny_white_lines, canny_yellow_lines, number_of_slices, 0, canny_white_lines.shape[1], lane_image,  dynamic_coordinates_left, dynamic_coordinates_right)
		if right_line.shape[0] != 0:
			# print(right_line)
			line_image_right = RI.display_lines_3D(lane_image, right_line, (0,0,255))
			# x_right_line, y_right_line = RI.stich_lines_of_slices_together(right_line, lane_image)
		else:
			line_image_right = lane_image
			# print("no_right")
		
		if left_line.shape[0] != 0:
			line_image_left = RI.display_lines_3D(lane_image, left_line, (0,255, 0))
			# x_left_line, y_left_line = RI.stich_lines_of_slices_together(left_line, lane_image)
			# print()
		else:
			line_image_left = lane_image
			# print("no_left")
		# print("RIGHT_LINE")
		# print(right_line)
		# print("LEFT_LINE")
		# print(left_line)
		lines_to_average_right = right_line
		# print(lines_to_average)
		# print("left_line.shape")
		# print(left_line.shape)
		# print("right_line.shape")
		# print(right_line.shape)
		# print("lines_to_average.shape")
		lines_to_average_right = np.array(lines_to_average_right)
		# lines_to_average_right = np.average(lines_to_average)
		# print(lines_to_average_right)
		# print(lines_to_average.shape)
		lines_to_average_left = left_line
		lines_to_average_left = np.array(lines_to_average_left)
		# lines_to_average_left = np.concatenate((lines_to_average, left_line), axis = 0)
		# print(lines_to_average)
		# lines_to_average = np.array(lines_to_average)
		left_offset = 250
		right_offset = -150
		offset = 0
		if left_line.shape[0] != 0 and right_line.shape[0] != 0: #this means I have a left and right line
			average_line_left = [np.average(lines_to_average_left[:,:,0]), np.average(lines_to_average_left[:,:,1]), np.average(lines_to_average_left[:,:,2]), np.average(lines_to_average_left[:,:,3])]
			average_line_right = [np.average(lines_to_average_right[:,:,0]), np.average(lines_to_average_right[:,:,1]), np.average(lines_to_average_right[:,:,2]), np.average(lines_to_average_right[:,:,3])]
			if average_line_right[0] < average_line_left[0] or average_line_right[2] < average_line_left[2] or average_line_right[1] < average_line_left[2] or average_line_right[2] < average_line_left[1]:
				steering_point = [int(average_line_left[2] + left_offset), int(average_line_left[3])]
			else:
				both_lines_to_average = [[average_line_left]]
				both_lines_to_average = np.concatenate((both_lines_to_average, [[average_line_right]]), axis = 0)
				# print(both_lines_to_average)
				average_line = [np.average(both_lines_to_average[:,:,0]), np.average(both_lines_to_average[:,:,1]), np.average(both_lines_to_average[:,:,2]), np.average(both_lines_to_average[:,:,3])]
				# average_line_left = [np.average(lines_to_average[:,:,2]), np.average(lines_to_average[:,:,3])]
				# average_line_right = [np.average(lines_to_average[:,:,0]), np.average(lines_to_average[:,:,1])]
				if left_line.shape[0] > right_line.shape[0]: # more left lines so adjust it to the right a little
					offset = 0
					# print("LEFT")
				elif left_line.shape[0] < right_line.shape[0]: # more RIGHT lines so adjust it to the LEFT a little
					offset = 0
					# print("RIGHT")
				steering_point = [int(average_line[2] + offset), int(average_line[3])]
				# print(average_line)
		elif left_line.shape[0] != 0 and right_line.shape[0] == 0: # I only have the left line
			average_line = [np.average(lines_to_average_left[:,:,0]), np.average(lines_to_average_left[:,:,1]), np.average(lines_to_average_left[:,:,2]), np.average(lines_to_average_left[:,:,3])]
			steering_point = [int(average_line[2] + left_offset), int(average_line[3])]

		elif left_line.shape[0] == 0 and right_line.shape[0] != 0: # I only have the right line
			average_line = [np.average(lines_to_average_right[:,:,0]), np.average(lines_to_average_right[:,:,1]), np.average(lines_to_average_right[:,:,2]), np.average(lines_to_average_right[:,:,3])]
			steering_point = [int(average_line[2] + right_offset), int(average_line[3])]
			
		else: #this is a defualt value
			steering_point = (500,300)

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
		# if closest_line_found is not None:
		# 	if len(closest_line_found) > 1:
		# 		print(closest_line_found)
		# 		if closest_line_found.any() > intersection_theshold:
		# 			#excecute turn or straight through intersection
		# 			print("Found intersection")
		# 			if turnIndex == 0:
		# 				straight_through_intersection()
		# 			elif turnIndex == 1:
		# 				turn_left_through_intersection()
		# 			elif turnIndex == 2:
		# 				straight_through_intersection()
		# 			elif turnIndex == 3:
		# 				turn_right_through_intersection()

		turnIndex = turnIndex+1
		if turnIndex > 3:
			turnIndex = 0
					


					 
		# print(steering_point)
		cv2.circle(lane_image, (steering_point[0], steering_point[1]), 10, (255,255,255), -1) #the color is organized as (blue, green, red)
		combo_image_lines = cv2.addWeighted(line_image_left, 0.5, line_image_right, 0.5, 1)
		# lane_image = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
		combo_image = cv2.addWeighted(lane_image, 0.3, combo_image_lines, 1, 1)
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

	#	plt.imshow(combo_image)
		#plt.show()

                
		# cv2.imshow("result", combo_image)
		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 	cap.release()
		# 	cv2.destroyAllWindows()
		# 	print("bar")
		# 	break
	steering_angle = steering_angle / FRAMES_TO_AVERAGE
	toleranceDeg = 5
	prevLine = None
	prevLineSearchTolerance = 20

	#Added this code to find what intersection we are in - Dylan
	#ils.useLaneNumber(wpm.reachedIntersection(getCoor("Green")))



	# RI.detectIntersection(canny_white_lines, toleranceDeg, prevLine, prevLineSearchTolerance)

	print(steering_angle)
	
	steer(steering_angle)
	#pub.publish(steering_angle)
	#rate.sleep()

