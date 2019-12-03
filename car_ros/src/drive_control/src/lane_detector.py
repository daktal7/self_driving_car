#!/usr/bin/env python
#Python_MainV5
# Python Main
import roadDetectV4
from roadDetectV4 import road_image as RI
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
		# self.W = None
		# self.H = None
		# self.writer = None
		# self.writer_2 = None
		self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		self.writer = cv2.VideoWriter("./Zach_Wes_test.avi", self.fourcc, 30,
										 (640, 480), True) 
		self.writer_2 = cv2.VideoWriter("./Zach_Wes_test_2.avi", self.fourcc, 30,
										 (640, 480), True) 

	def shutDown(self):
		print("SHUTTING DOWN LANE_DETECTOR")
		self.writer.release()
		self.writer_2.release()

	def display(self, data):
		global dynamic_coordinates_right, dynamic_coordinates_left

		frame = self.bridge.imgmsg_to_cv2(data, "rgb8")
		if frame is None:
			return
		if self.count == 0:
			#start = time.time()
			image = cv2.resize(frame, (640, 480))

			lane_image = np.copy(image)
			canny_white_lines, canny_yellow_lines = RI.getCanny(lane_image)
			right_line, left_line, test_image = RI.split_detect(canny_white_lines, canny_yellow_lines, number_of_slices, 0, canny_white_lines.shape[1], lane_image, dynamic_coordinates_left, dynamic_coordinates_right)
			if right_line.shape[0] != 0:
				line_image_right = RI.display_lines_3D(lane_image, right_line, (0, 0, 255))
			else:
				line_image_right = lane_image
			if left_line.shape[0] != 0:
				line_image_left = RI.display_lines_3D(lane_image, left_line, (0, 255, 0))
			else:
				line_image_left = lane_image
			lines_to_average_right = right_line
			lines_to_average_right = np.array(lines_to_average_right)
			lines_to_average_left = left_line
			lines_to_average_left = np.array(lines_to_average_left)
			left_offset = 155
			right_offset = -220
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
			if left_line.shape[0] != 0:  # and right_line.shape[0] == 0: # I only have the left line
				average_line = [np.average(lines_to_average_left[:, :, 0]), np.average(lines_to_average_left[:, :, 1]),
								np.average(lines_to_average_left[:, :, 2]), np.average(lines_to_average_left[:, :, 3])]
				steering_point = [int(average_line[2] + left_offset), int(average_line[3] + 15)]


			elif left_line.shape[0] == 0 and right_line.shape[0] != 0:  # I only have the right line
				average_line = [np.average(lines_to_average_right[:, :, 0]),
								np.average(lines_to_average_right[:, :, 1]),
								np.average(lines_to_average_right[:, :, 2]),
								np.average(lines_to_average_right[:, :, 3])]
				steering_point = [int(average_line[2] + right_offset), int(average_line[3])]

			else:  # this is a defualt value
				steering_point = (370, 300)

			fudge_factor = 50
			if steering_point[0] > lane_image.shape[1] + fudge_factor:
				steering_point[0] = lane_image.shape[1] + fudge_factor
			if steering_point[1] > lane_image.shape[0] + fudge_factor:
				steering_point[1] = lane_image.shape[0] + fudge_factor
			steering_angle = RI.getDriveAngle(steering_point)
			# Check for intersection
			#toleranceDeg = 5
			#prevLine = None
			#prevLineSearchTolerance = 20
			# closest_line_found = RI.detectIntersection(canny_white_lines, toleranceDeg, prevLine, prevLineSearchTolerance)
			intersection_theshold = 410

			#cv2.circle(lane_image, (steering_point[0], steering_point[1]), 10, (255, 255, 255),
			#		   -1)  # the color is organized as (blue, green, red)
			#combo_image_lines = cv2.addWeighted(line_image_left, 0.5, line_image_right, 0.5, 1)
			#combo_image = cv2.addWeighted(lane_image, 0.3, combo_image_lines, 1, 1)

			# if self.W is None or self.H is None:
			#     (self.H, self.W) = frame.shape[:2]

			# check if the video writer is None
			# if self.writer is None:
			# 	# initialize our video writer
			# 	fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			# 	self.writer = cv2.VideoWriter("./Zach_Wes_test.avi", fourcc, 30,
			# 							 (640, 480), True) 
			# 	print("Initializing WRITER")
			# if self.writer_2 is None:
			# 	# initialize our video writer
			# 	fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			# 	self.writer_2 = cv2.VideoWriter("./Zach_Wes_test_2.avi", fourcc, 30,
			# 							   (640, 480), True)

			# write the output frame to disk
			#test_image = RI.filter_yellow(frame)

			#test_image = cv2.cvtColor(test_image, cv2.COLOR_GRAY2RGB)
			#test_image_resized = cv2.resize(test_image, (640, 480))
			#self.writer.write(test_image_resized)
			#self.writer.write(test_image_resized)
			#self.writer.write(test_image_resized)

			#self.writer_2.write(combo_image)

			# cv2.imshow("result", combo_image)
			# cv2.waitKey(1)

			self.angle_pub.publish(steering_angle)
			#end = time.time()
			#print("time elapsed: ", end - start)

			#self.count = self.count + 1
			self.count = 1

		elif self.count == 1:
			self.count = 0
		else:
			self.count = 0


FRAMES_TO_AVERAGE = 3
DRIVING_SPEED = 0.05
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

rospy.init_node('lane_detector', anonymous = True)
id = image_displayer()
rospy.spin()
rospy.on_shutdown(id.shutDown)



#self.angle_pub.publish(steering_angle)
