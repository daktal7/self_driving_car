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

ROI = 170/613;
BLACK_THRESH = 20
BIN_THRESH = .6
RES = 100

GREEN_CENTER = 60
GREEN_BUFFER = 20
GREEN_LOWER = GREEN_CENTER-GREEN_BUFFER
GREEN_UPPER = GREEN_CENTER+GREEN_BUFFER+10
SAT_CUTOFF = 150
GREEN_CUTOFF = 100

class tlDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("video_topic", Image, self.light_detect)
        self.intersection_sub = rospy.Subscriber("intersection", Int32, self.intersect)
        self.light_pub = rospy.Publisher('light', Bool, queue_size = 1)
        self.intersection = False
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
        print(resGreen)
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
            #print("tlDetect: returning none")
            return None
        return im[0:int(ROI*len(im[:,0])),(maxI-iLeft)*dx:(maxI+iRight)*dx,:]

    #im must be hsv, res is how many cross sections are made
    #will return numpy array that contains just the traffic light
    def getTL(self, im):
        bins = np.zeros((RES,2))
        dx = len(im[0,:])//RES
        yWindow = int(ROI*len(im[:,0]))
        print("yWindow: ",yWindow)
        print("roi: ", ROI)
        print("len: ", len(im[:,0]))
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
        return self.getBox(im,bins,maxI,dx)

    def intersect(self, data):
        if data.data == 4:
           self.intersection = True
            # time.sleep(10)
            # self.intersection = False
        

    def light_detect(self, data):
        if self.intersection == False:
            #print("not in the intersection")
            return
        print("In light_detect")
        im = self.bridge.imgmsg_to_cv2(data,"rgb8")
        if im is None:
            print("bad image")
            return 
        #try:
        hsvIm = cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
        #print("hsv shape:", np.shape(hsvIm))
        #except:
        #    print("Failed to convert to hsv")
        #    return
        if hsvIm is None:
            print("hsv is none")
            return
        #try:
            #print(hsvIm)
        light = self.getTL(hsvIm)
        #except:
        #    print("failed to get TL")
        #    return
        # print(light.length())
        #try:
        if light is not None:
            green = self.isGreen(light)
            print(green)
            self.light_pub.publish(green)
            # if(green):
                # self.intersection = False
        #except:
        #    print("Failed to check for green")
        # roi = 170/len(hsvIm[:,0])

        # cv2.imshow("Traffic Light", im)
        # key = cv2.waitKey(1) & 0xFF

        # if key == ord("q"):
        #     break
        # plt.figure()

        # plt.imshow(im)

        # plt.figure()
        # plt.imshow(cv2.cvtColor(light,cv2.COLOR_HSV2RGB))

        # plt.show()

tl = tlDetector()
rospy.init_node('light_node', anonymous=False)
rospy.spin()
