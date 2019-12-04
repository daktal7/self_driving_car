#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32, Int32, Bool
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
OBJECT_DETECTED = False
WARNING_INTERSECTION = False
ANGLE_THRESHOLD = 12
DRIVE_SPEED = 0.008
STARTUP_SPEED = .0095
GREEN = False
prevAngle = 0


# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    print('CTRL-C detected. Exiting gracefully')
    exit(0)


def steer(angle):
    if OBJECT_DETECTED:
        return
    global DRIVE_LOCK
    if WARNING_INTERSECTION:
        print("WARNING_INTERSECTION:")
        if abs(angle.data) > ANGLE_THRESHOLD:
            DRIVE_LOCK = True
            print("Drive Lock Engagded")
    if not DRIVE_LOCK:
        # print(angle.data)
        if WARNING_INTERSECTION:
            print(angle.data)
        command = "!steering" + str(angle.data) + "\n"
        ser.write(command.encode())

def drive(speed):
    # if not DRIVE_LOCK:
    command = "!speed" + str(speed) + "\n"
    ser.write(command.encode())


def turn_right_stop_sign():
    global DRIVE_LOCK
    angle = 2.5 - prevAngle/2
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(STARTUP_SPEED)
    time.sleep(1)
    angle = 30 - prevAngle
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(DRIVE_SPEED)
    time.sleep(2.4)
    DRIVE_LOCK = False
    print("Drive lock disengaged")


def turn_right_intersection():
    print("Running turn_right_instersection")
    global DRIVE_LOCK
    angle = 2.5 - prevAngle/2
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(STARTUP_SPEED)
    time.sleep(2)
    print("Done with straight part of right turn")
    angle = 30 - prevAngle
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(DRIVE_SPEED)
    time.sleep(2.4)
    DRIVE_LOCK = False
    print("drive lock disengaged")


def turn_left():
    global DRIVE_LOCK
    drive(STARTUP_SPEED)
    time.sleep(1.5)
    angle = -20 - prevAngle
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(DRIVE_SPEED)
    time.sleep(2)
    DRIVE_LOCK = False
    print("drive lock disengaged")


def go_straight():
    global DRIVE_LOCK
    angle = 2.5 - prevAngle/2
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(STARTUP_SPEED)
    time.sleep(4)
    drive(DRIVE_SPEED)
    DRIVE_LOCK = False
    print("drive lock disengaged")


def intersect(turn):
    if OBJECT_DETECTED:
        return
    global DRIVE_LOCK,WARNING_INTERSECTION
    if turn.data == 4:
        WARNING_INTERSECTION = True
    else:
        WARNING_INTERSECTION = False
    # for i in range(0,50):
    #     print(i)
    #GREEN = True
    if GREEN:
        if turn.data == -1:
            print("Drive: turn left")
            turn_left()
        if turn.data == 0:
            print("Drive: go straight")
            go_straight()
        if turn.data == 1:
            print("Drive: turn right intersection")
            turn_right_intersection()
        if turn.data == 40:
            print("Drive: turn right stop sign")
            turn_right_stop_sign()
    if turn.data == 2:
        print("Drive: stop")
        drive(0)

def emergencyStop(flag):
    global OBJECT_DETECTED
    print("got an emergency stop flag")
    if flag.data == 1:
        if not OBJECT_DETECTED:
            print("stopping for object")
            OBJECT_DETECTED = True
            drive(0)
    else:
        if OBJECT_DETECTED:
            print("object gone, starting")
            OBJECT_DETECTED = False
            drive(DRIVE_SPEED)

def stopLight(light):
	global GREEN
	if light.data:
		GREEN = True
	else:
		GREEN = False


def drive_control():
    print("drive_control here")
    rospy.init_node('drive_control', anonymous=False)
    # subscribe to whatever is checking our intersections
    # rospy.Subscriber("intersectionNumber", int, inter.useLaneNumber)
    rospy.Subscriber("steerAngle", Float32, steer)
    #rospy.Subscriber("driveSpeed", Float32, drive)
    rospy.Subscriber("intersection", Int32, intersect)
    rospy.Subscriber("Emergency_Stop",Int32, emergencyStop)
    rospy.Subscriber("light", Bool, stopLight)

    rospy.spin()


if __name__ == '__main__':
    # initialize communication with the arduino
    ser = serial.Serial("/dev/ttyUSB0", 115200)
    ser.flushInput()
    time.sleep(2)

    print("about to init")
    # will need to change because of new gear ratios
    init_command = "!start1635\n"  # was 1750 // was 1615
    ser.write(init_command.encode())
    init_command = "!inits.002\n"
    ser.write(init_command.encode())
    init_command = "!kp0.01\n"
    ser.write(init_command.encode())
    init_command = "!kd0.01\n"
    ser.write(init_command.encode())
    init_command = "!pid0\n"
    ser.write(init_command.encode())
    init_command = "!speed.0075\n"
    ser.write(init_command.encode())

    time.sleep(.25)
    drive(0)  # Stop and wait for a second
    time.sleep(1)
    drive(DRIVE_SPEED)

    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit')
    drive_control()
    # while True:
    # steer(0)
    # time.sleep(1)
    # drive(0.5)
    # time.sleep(2)
    # steer(30)
    # time.sleep(1)
    # steer(0)
    # time.sleep(1)
    # drive(0)
    # time.sleep(1)
