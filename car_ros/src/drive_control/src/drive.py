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
import intersectionLaneSwitches as inter

DRIVE_LOCK = False	

# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    vs.release()
    print('CTRL-C detected. Exiting gracefully')
    exit(0)

def steer(angle):
    if not DRIVE_LOCK:
        #print(angle.data)
        command = "!steering" + str(angle.data) + "\n"
        ser.write(command.encode())

def drive(speed):
    if not DRIVE_LOCK:
        print("speed ",speed)
        command = "!speed" + str(speed.data) + "\n"
        ser.write(command.encode())

def turn_right():
	steer(30)
	time.sleep(1)

def turn_left():
	steer(-20)
	time.sleep(0.75)

def go_straight():
	steer(0)
	time.sleep(1)


def intersect(turn):
    print("in drive intersection")
    global DRIVE_LOCK
    DRIVE_LOCK = True
    if turn.data == -1:
        print("Drive: turn left")
        turn_left()
    if turn.data == 0:
        print("Drive: go straight")
        go_straight()
    if turn.data == 1:
        print("Drive: turn right")
        turn_right()
    if turn.data == 2:
        print("Drive: stop")
        drive(0)

def drive_control():
    print("drive_control here")
    rospy.init_node('drive_control', anonymous=False)
    #subscribe to whatever is checking our intersections
    #rospy.Subscriber("intersectionNumber", int, inter.useLaneNumber)
    rospy.Subscriber("steerAngle", Float32, steer)
    rospy.Subscriber("driveSpeed", Float32, drive)
    rospy.Subscriber("intersection", Float32, intersect)
    rospy.spin()

if __name__ == '__main__':
# initialize communication with the arduino
	ser = serial.Serial("/dev/ttyUSB0",115200)
	ser.flushInput()
	time.sleep(2)

	print("about to init")
	#will need to change because of new gear ratios
	init_command = "!start1615\n"# was 1750
	ser.write(init_command.encode())
	init_command = "!inits.002\n"
	ser.write(init_command.encode())
	init_command = "!kp0.01\n"
	ser.write(init_command.encode())
	init_command = "!kd0.01\n"
	ser.write(init_command.encode())
	init_command = "!pid0\n"
	ser.write(init_command.encode())
	init_command = "!speed.3\n"
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
