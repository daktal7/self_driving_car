#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import rospy 
import time
from std_msgs.msg import Bool, Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

ROI = 170.0/613.0;
BLACK_THRESH = 20
BIN_THRESH = .3
RES = 100

GREEN_CENTER = 60
GREEN_BUFFER = 20
GREEN_LOWER = GREEN_CENTER-GREEN_BUFFER
GREEN_UPPER = GREEN_CENTER+GREEN_BUFFER+10
SAT_CUTOFF = 200
GREEN_CUTOFF = 150
TIMEOUT_LIM = 30

class tlDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("TL_video", Image, self.light_detect)
        #self.intersection_sub = rospy.Subscriber("intersection", Int32, self.intersect)
        self.light_pub = rospy.Publisher('light', Bool, queue_size = 10)
        self.intersection = False
        self.frameCount = 0
        self.frameMod = 20
        self.timeOut = 0
    # im must be in hsv
    #returns 'r' for red and 'g' for green
    #if box is none the algorithm will run over the entire image
    #commented out stuff used for debugging
    def isGreen(self,im):
        resGreen = 0
        #light = np.zeros((box[2]-box[0],box[3]-box[1],3),np.uint16)
        for i in range(len(im[:,0])):
            for j in range(len(im[0,:])):
                #hsvPix = cv2.cvtColor(np.array([[im[i, j]]]), colorFormat)#YOU MAY NEED TO SWITCH THE J AND THE I
                if GREEN_LOWER <= im[i, j, 0] <= GREEN_UPPER and im[i, j, 1] > SAT_CUTOFF:
                    resGreen = resGreen + 1
                    # light[i - box[0], j - box[1], 1] = 255
        print("tlDetect: resgreen ", resGreen)
        if resGreen > GREEN_CUTOFF:
            return True
        return False

    def getNumBlack(self,im):
        res = 0
        #print("numbBlack image size:", np.shape(im))
        for i in range(len(im[:,0])):
            for j in range(len(im[0,:])):
                if im[i,j] < BLACK_THRESH:
                    res = res+1
        return res

    def getBox(self,im,bins,maxI,dx):
        iRight = 0
        iLeft = 0
        if maxI < len(bins[:,0]):
            for i in range(maxI+1,len(bins)):
                if bins[i,1] > BIN_THRESH*bins[maxI,1]:
                    iRight = iRight + 1
                else:
                    break
        if maxI > 0:
            for i in range(maxI-1,-1,-1):
                if bins[i,1] > BIN_THRESH*bins[maxI,1]:
                    iLeft = iLeft + 1
                else:
                    break
        if iRight == 0 and iLeft == 0:
            print("tlDetect: returning none")
            return None
        print("maxI: ", maxI)
        print("iRight: ", iRight)
        print("iLeft: ", iLeft)
        return im[0:int(ROI*len(im[:,0])),(maxI-iLeft)*dx:(maxI+iRight)*dx,:]

    #im must be hsv, res is how many cross sections are made
    #will return numpy array that contains just the traffic light
    def getTL(self, im):
        bins = np.zeros((RES,2))
        dx = len(im[0,:])//RES
        yWindow = int(ROI*len(im[:,0]))
        #print("dx val:", dx)
        maxVal = 0
        maxI = -1
        for i in range(RES):
            bins[i,0] = i
            bins[i,1] = self.getNumBlack(im[0:yWindow,i*dx:i*dx+dx,2])
            if bins[i,1] > maxVal:
                maxVal = bins[i,1]
                maxI = i
        #print("tlDetect: bins", bins)
        print("tlDetect: maxBlack ", maxVal)
        return self.getBox(im,bins,maxI,dx)

    def intersect(self, data):
        if data.data == 5:
           if self.intersection == False:
                print("tlDetect: turningn light detection on")
           self.intersection = True
            # time.sleep(10)
            # self.intersection = False
        

    def light_detect(self, data):
        if self.timeOut == 0:
            self.timeOut = time.time()
        #    self.frameCount = 0
            #print("not in the intersection")
        #    return

        self.frameCount = self.frameCount + 1
        #print("TLDEtect, Framecount: ", frameCount)
        if self.frameCount % self.frameMod:
            return
        #print("In light_detect")
        hsvIm = self.bridge.imgmsg_to_cv2(data)

        if hsvIm is None:
            print("hsv is none")
            return
        green = self.isGreen(hsvIm[0:int(ROI * len(hsvIm[:, 0])), :])
        if (time.time() - self.timeOut) > TIMEOUT_LIM:
            print("Green Timed-out")
            green = True

        #time.sleep(1) #disabling light detection for now,
        #green = True #comment these lines out to enable light detection

        print("tlDetect: is green?", green)
        self.light_pub.publish(green)
        self.timeOut = 0
        if green:
            self.frameCount = 0
            #self.intersection = False
            #print("tlDetect: disabling light detection")



tl = tlDetector()
rospy.init_node('light_node', anonymous=False)
rospy.spin()
