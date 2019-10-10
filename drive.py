from car_control import steer, drive
from matplotlib import pyplot as plt
# from gluoncv import model_zoo, utils
# import pyrealsense2 as rs
# from PIL import Image
from signal import signal, SIGINT
from sys import exit
import numpy as np
import mxnet as mx
import argparse
import imutils
import serial
import time
# import cv2
import os
import gc

# Function to correctly exit program
def handler(signal_received, frame):
    vs.release()
    print('CTRL-C detected. Exiting gracefully')
    exit(0)

# initialize communication with the arduino
ser = serial.Serial("/dev/ttyUSB0",115200)
ser.flushInput()
time.sleep(2)

signal(SIGINT, handler)
print('Running. Press CTRL-C to exit')

steer(0)
drive(1500)
