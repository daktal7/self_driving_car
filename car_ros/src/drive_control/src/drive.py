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
GPS_FAILED = False
WARNING_INTERSECTION = False
ANGLE_THRESHOLD = 12
DRIVE_SPEED = 0.0076
STARTUP_SPEED = .0095
RES = 100
GREEN = False
STORED_TURN = -100 #junk value
prevAngle = 0


# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    print('CTRL-C detected. Exiting gracefully')
    exit(0)


def steer(angle):
    if OBJECT_DETECTED or GPS_FAILED:
        return
    global DRIVE_LOCK
    if WARNING_INTERSECTION:
        #print("WARNING_INTERSECTION:")
        if abs(angle.data) > ANGLE_THRESHOLD:
            DRIVE_LOCK = True
            print("Drive Lock Engagded")
    if not DRIVE_LOCK:
        #if WARNING_INTERSECTION:
            #print(angle.data)
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
    straightTime = 1
    rightTime = 2.4
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(straightTime / RES)
    angle = 30 - prevAngle
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(rightTime / RES)
    drive(DRIVE_SPEED)
    DRIVE_LOCK = False
    print("Drive lock disengaged")


def turn_right_intersection():
    print("Running turn_right_instersection")
    global DRIVE_LOCK
    angle = 2.5 - prevAngle/2
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(STARTUP_SPEED)
    straightTime = 2
    rightTime = 2.8
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(straightTime / RES)
    angle = 30 - prevAngle
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    print("Done with straight part of right turn")
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(rightTime / RES)
    drive(DRIVE_SPEED)
    DRIVE_LOCK = False
    print("drive lock disengaged")


def turn_left():
    global DRIVE_LOCK
    drive(STARTUP_SPEED)
    angle = 2.5 - prevAngle/2
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())     #was 2, was 1.5, added a bit more straight time so it would not clip the corner of the other lane
    straightTime = 2.5
    leftTime = 2.8
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(straightTime / RES)
    angle = -20 - prevAngle
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(leftTime / RES)
    drive(DRIVE_SPEED)
    DRIVE_LOCK = False
    print("drive lock disengaged")


def go_straight():
    print("drive: Beginning Straight")
    global DRIVE_LOCK
    angle = 2.5 - prevAngle/2
    command = "!steering" + str(angle) + "\n"
    ser.write(command.encode())
    drive(STARTUP_SPEED)
    straightTime = 5.0
    #time.sleep(4)
    for i in range(RES):
        if OBJECT_DETECTED:
            drive(0)
            while OBJECT_DETECTED:
                continue
            drive(STARTUP_SPEED)
        time.sleep(straightTime/RES)
    drive(DRIVE_SPEED)
    DRIVE_LOCK = False
    print("straight: drive lock disengaged")


def intersect(turn):
    global STORED_TURN, DRIVE_LOCK, GREEN, OBJECT_DETECTED, GPS_FAILED
    STORED_TURN = turn
    if OBJECT_DETECTED or GPS_FAILED:
        return
    global DRIVE_LOCK,WARNING_INTERSECTION
    if turn.data == 4:
        WARNING_INTERSECTION = True
    else:
        WARNING_INTERSECTION = False
    # for i in range(0,50):
    #     print(i)
    if turn.data == 6:
        print("Drive: GPS BROKEN, STOPPING")
        GPS_FAILED = True
        drive(0)
    if turn.data == 7:
        print("Drive: GPS recovered")
        GPS_FAILED = False
        drive(DRIVE_SPEED)
    if turn.data == 40:
        print("Drive: turn right stop sign")
        turn_right_stop_sign()
    if turn.data == -40:
        print("Drive: turn left stop sign")
        turn_left()
    if turn.data == 2:
        DRIVE_LOCK = True
        print("Drive: stop")
        drive(0)
    #GREEN = True
    if GREEN:
        if turn.data == -1:
            print("Drive: turn left")
            turn_left()
        if turn.data == 0:
            print("Drive: go straight")
            go_straight()
        if turn.data == 1:
            print("Drive: turn right stop light")
            turn_right_intersection()
        GREEN = False

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
            print("drive: object gone, starting")
            OBJECT_DETECTED = False
            drive(DRIVE_SPEED)


def stopLight(light):
    global GREEN
    if light.data:
        GREEN = True
        print("drive: setting green to true")
        intersect(STORED_TURN)
        GREEN = False
    else:
        GREEN = False


def drive_control():
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
    init_command = "!start1635\n"  # was 1750 // was 1615 // was 1632
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
