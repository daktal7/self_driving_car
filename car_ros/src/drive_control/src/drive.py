#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from matplotlib import pyplot as plt
# from gluoncv import model_zoo, utils
# import pyrealsense2 as rs
# from PIL import Image
from signal import signal, SIGINT
from sys import exit
import numpy as np
# import mxnet as mx
import argparse
import imutils
import serial
import time
# import cv2
import os
import gc

# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    vs.release()
    print('CTRL-C detected. Exiting gracefully')
    exit(0)

def steer(angle):
    print(angle.data)
    command = "!steering" + str(angle.data) + "\n"
    ser.write(command.encode())

def drive(speed):
    command = "!speed" + str(speed.data) + "\n"
    ser.write(command.encode())

def drive_control():
    rospy.init_node('drive_control', anonymous=False)
    rospy.Subscriber("steerAngle", Float32, steer)
    rospy.Subscriber("driveSpeed", Float32, drive)
    rospy.spin()



if __name__ == '__main__':
# initialize communication with the arduino
	ser = serial.Serial("/dev/ttyUSB0",115200)
	ser.flushInput()
	time.sleep(2)

	init_command = "!start1750\n"
	ser.write(init_command.encode())
	init_command = "!inits1.5\n"
	ser.write(init_command.encode())
	init_command = "!kp0.01\n"
	ser.write(init_command.encode())
	init_command = "!kd0.01\n"
	ser.write(init_command.encode())
	init_command = "!pid1\n"
	ser.write(init_command.encode())
	init_command = "!speed.4\n"
	ser.write(init_command.encode())


	signal(SIGINT, handler)
	print('Running. Press CTRL-C to exit')
	drive_control()
	#while True:
	#steer(0)
	#time.sleep(1)
	#drive(0.5)
	#time.sleep(2)
	#steer(30)
	#time.sleep(1)
	#steer(0)
	#time.sleep(1)
	#drive(0)
	#time.sleep(1)
