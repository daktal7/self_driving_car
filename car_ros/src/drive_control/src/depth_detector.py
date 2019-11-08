#!/usr/bin/env python
#Python_MainV5
# Python Main
import roadDetectV4
from roadDetectV4 import road_image as RI
import cv2
import matplotlib.image as mpimg
import math
import serial
import time
from signal import signal, SIGINT
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32


from std_msgs.msg import Float32, Int32
from matplotlib import pyplot as plt
from signal import signal, SIGINT
from sys import exit
import numpy as np
from drive import drive
import argparse
import imutils
import os
import gc
import intersectionLaneSwitches as inter


class image_displayer:
	def __init__(self):
		self.bridge = CvBridge()
		self.depth_image_sub = rospy.Subscriber("depth_video_topic", Image, self.display_depth)
		#self.image_sub = rospy.Subscriber("video_topic", Image, self.display)
		#self.emergency_stop_pub = rospy.Publisher("Emergency_Stop", Float32, queue_size = 1)
		self.count = 0

	def display_depth(self, data):
		global dynamic_coordinates_right, dynamic_coordinates_left
		frame = self.bridge.imgmsg_to_cv2(data, "16UC1")
		if frame is None:
			return
		if self.count == 0:
			start = time.time()
			image = cv2.resize(frame, (640, 480))

			depth_image = np.copy(image)
			#depth_image = np.asanyarray(depth_frame.get_data())
			depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
			threshold_value = 145
			self.check_for_obstacles(depth_colormap, threshold_value)
		
	def region_of_interest_depth(self, depth_image):
		height = depth_image.shape[0]
		width = depth_image.shape[1]
		mask = np.zeros_like(depth_image)
		right_in_front_of_us = np.array([[(200, 150), (200, 380), (440, 380), (440, 150)]])
		cv2.fillPoly(mask, right_in_front_of_us, 255)
		masked_image = cv2.bitwise_and(depth_image, mask)
		return masked_image

	def check_for_obstacles(self, depth_image, threshold_value):		
		obstacle_detected_threshold = 10500
		ret, threshold_image = cv2.threshold(depth_image, threshold_value, 255, cv2.THRESH_BINARY_INV)
		masked_depth_image = self.region_of_interest_depth(threshold_image)
			
		cv2.imshow("depth_thresh", masked_depth_image)
		cv2.waitKey(1)
		threshold_image_gray = cv2.cvtColor(masked_depth_image, cv2.COLOR_RGB2GRAY)
		number_of_obstacle_pixels = 10
		number_of_obstacle_pixels = cv2.countNonZero(threshold_image_gray)
		if number_of_obstacle_pixels > obstacle_detected_threshold:
			#there is an obstacle ahead STOP now
			print("STOP!!")
			#drive(0)
		else:
			#path is clear
			#drive(Driving_speed)
			###################   FIX THIS SO IT CAN ACTUALLY CALL drive()

rospy.init_node('depth_detector', anonymous = True)
id = image_displayer()
rospy.spin()



#self.angle_pub.publish(steering_angle)
