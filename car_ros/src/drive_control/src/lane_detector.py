#!/usr/bin/env python
#Python_MainV5
# Python Main
import roadDetectV5
from roadDetectV5 import road_image as RI
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import serial
import time
from signal import signal, SIGINT
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32


class image_displayer:
	def __init__(self):
		self.bridge = CvBridge()		
		self.image_sub = rospy.Subscriber("video_topic", Image, self.display)
		self.angle_pub = rospy.Publisher("steerAngle", Float32, queue_size = 1)
		self.count = 0
	
	def display(self, data):
		frame = self.bridge.imgmsg_to_cv2(data, "rgb8")
		if frame is None:
			return
		if self.count == 0:
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
			left_offset = 100 #Lower this again if the lanes is still too close to the right
			right_offset = -250
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


			if steering_point[0] > lane_image.shape[1]:
				steering_point[0] = lane_image.shape[1]
			if steering_point[1] > lane_image.shape[0]:
				steering_point[1] = lane_image.shape[0]
			steering_angle = RI.getDriveAngle(steering_point)
			self.angle_pub.publish(steering_angle)
			# Check for intersection
			toleranceDeg = 6
			prevLine = None
			prevLineSearchTolerance = 20
			closest_line_found = RI.detectIntersection(canny_white_lines, toleranceDeg, prevLine, prevLineSearchTolerance)
			intersection_theshold = 400
			intersection_theshold_x = 400
			# print(closest_line_found)
			if closest_line_found is not None:
				# print(closest_line_found)
				if closest_line_found[0][0][1] > intersection_theshold:
					avg_thing = (closest_line_found[0][0][0] + closest_line_found[0][0][2])/ 2
					if avg_thing - 50 < intersection_theshold_x and avg_thing + 50 > intersection_theshold_x:
						#if Frames_since_last_intersection > 100:
							#excecute turn or straight through intersection
						print("Found intersection")
						#	print("Index is: " + str(turnIndex))
						#	if turnIndex == 0:
						#		straight_through_intersection()
						#	elif turnIndex == 1:
						#		turn_left_through_intersection()
						#	elif turnIndex == 2:
						#		straight_through_intersection()
						#	elif turnIndex == 3:
						#		turn_right_through_intersection()
						#	Frames_since_last_intersection = 0
						#	turnIndex = turnIndex + 1
						#	if turnIndex > 3:
						#		turnIndex = 0



						 
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

			#plt.imshow(combo_image)
			#plt.show()
			self.count = 1
			        
			#cv2.imshow("result", combo_image)
			#if cv2.waitKey(1) & 0xFF == ord('q'):
				#cap.release()
				#cv2.destroyAllWindows()
				#print("bar")
				#return
		elif self.count == 1:
			self.count = 2
		else:
			self.count = 0

		# toleranceDeg = 5
		# prevLine = None
		# prevLineSearchTolerance = 20
		# RI.detectIntersection(canny_white_lines, toleranceDeg, prevLine, prevLineSearchTolerance)

		#print(steering_angle)
		# speed(DRIVING_SPEED)
		#steer(steering_angle)
		#pub.publish(steering_angle)
		#rate.sleep()	

FRAMES_TO_AVERAGE = 3
DRIVING_SPEED = 0.27
Frames_since_last_intersection = 110

number_of_slices = 5
dynamic_coordinates_right = [[[123,123],[123,123],[123,123],[123,123]]]
dynamic_coordinates_left = [[[123,123],[123,123],[123,123],[123,123]]]
for num in range(number_of_slices):
    dynamic_coordinates_right = np.concatenate((dynamic_coordinates_right, [[[123,123],[123,123],[123,123],[123,123]]]), axis = 0)
    dynamic_coordinates_left = np.concatenate((dynamic_coordinates_left, [[[123,123],[123,123],[123,123],[123,123]]]), axis = 0)

# start of the Main
# yellow_pic
# frame = cv2.imread('color_wheel.png')

#cap = cv2.VideoCapture("roadTest2.avi")

#pub = rospy.Publisher('steerAngle', Float32, queue_size=10)
#rospy.init_node('angleTalker', anonymous=False)
#rate = rospy.Rate(10)

id = image_displayer()
rospy.init_node('lane_detector', anonymous = True)
rospy.spin()

