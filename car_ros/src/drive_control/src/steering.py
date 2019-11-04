#!/usr/bin/env python

import math
import numpy as np
import cv2

X = 0
Y = 1

CARNOSE = [.5918,.983] # this coordinate is normalized by the image width and height. In order to get the actual point,
                      # you need to multiply by image width and height

IMWIDTH = 640 #CHANGE THIS TO WHATEVER YOUR IMAGE SIZE IS
IMHEIGHT = 480 #CHANGE THIS TO WHATEVER YOUR IMAGE SIZE IS

ANGOFFSET = 8.85

p1_world = [-29.6, 78.9]
p2_world = [-19.7, 39.5]
p3_world = [19.7, 39.5]
p4_world = [19.7, 78.9]

p1_im = np.array([131/640, 276/480])*np.array([IMWIDTH,IMHEIGHT])
p2_im = np.array([112/640, 387/480])*np.array([IMWIDTH,IMHEIGHT])
p3_im = np.array([592/640, 392/480])*np.array([IMWIDTH,IMHEIGHT])
p4_im = np.array([471/640, 281/480])*np.array([IMWIDTH,IMHEIGHT])

src = np.array([p1_im, p2_im, p3_im, p4_im])
dst = np.array([p1_world, p2_world, p3_world, p4_world])

homMat,_ = cv2.findHomography(src,dst,method=0)

    # pt is just an array of size 2, [x,y]
    # negative is turn left, positive is turn right

# imPt is an array of form [x,y], returns array of form [x,y],
def getWorld(imPt):
    global homMat
    pt = np.array([imPt[0],imPt[1],1])
    res = np.dot(homMat,pt)
    res = res/res[2]
    return res[:2]

def getDriveAngleJimmy(pt):
    global CARNOSE,IMWIDTH,IMHEIGHT,ANGOFFSET
    dx = (CARNOSE[0]*IMWIDTH)-pt[0]
    dy = (CARNOSE[1]*IMHEIGHT)-pt[1]
    return -1*math.degrees(math.atan2(dx,dy))+ANGOFFSET

# pt is in pixel coordinates, [x,y]
def getDriveAngleHom(pt):
    ptWorld = getWorld(pt)
    return math.degrees(math.atan2(ptWorld[X],ptWorld[Y]))

def getDriveAngle(pt):
    return getDriveAngleHom(pt)

def testHom():
    tp1 = [343,320]
    tp2 = [62, 446]
    tp3 = [616, 443]
    tp4 = [601, 285]
    print("dr 1: ", getDriveAngle(tp1))
    print("dr 2: ", getDriveAngle(tp2))
    print("dr 3: ", getDriveAngle(tp3))
    print("dr 4: ", getDriveAngle(tp4))

testHom()