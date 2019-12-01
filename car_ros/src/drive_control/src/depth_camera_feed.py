#!/usr/bin/env python
import cv2
import time
from signal import signal, SIGINT
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import pyrealsense2 as rs
import numpy as np
#from std_msgs.msg import Float32

class image_converter_depth:
	def __init__(self):
		print("image_converter_depth")
		self.pipeline = rs.pipeline()
		self.config = rs.config()
		self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
		# Start streaming
		self.pipeline.start(self.config)
		self.image_pub = rospy.Publisher("depth_video_topic", Image, queue_size=1)
		self.bridge = CvBridge()
	
	def publish_frame(self):
		try:
			frames = self.pipeline.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			depth_image = np.asanyarray(depth_frame.get_data())
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(depth_image, "16UC1"))
			#self.image_pub.publish(self.bridge.cv2_to_imgmsg(frame, "rgb8"))
		except CvBridgeError as e:
			print(e)

# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    cap.release()
    print('CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)
print('Running. Press CTRL-C to exit')
cap = cv2.VideoCapture("/dev/video1",cv2.CAP_V4L)
icd = image_converter_depth()
rospy.init_node('video', anonymous = False)
while(cap.isOpened()):
	try:
		_, frame = cap.read()
		icd.publish_frame()
	except KeyboardInterrupt:
		print("Shutting Down Video")
		break
cv2.destroyAllWindows()


rospy.init_node('depth_video', anonymous = True)
id = image_displayer()
rospy.spin()
