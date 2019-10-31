#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import matplotlib.path as mpltPath

#this are the coordinates for all the intersections
INT_1 = np.array([[878, 454],[822, 395],[970, 259],[1023, 328]])
INT_2 = np.array([[ 834,  541],[ 952,  671],[ 899,  742],[ 773,  610]])
INT_3 = np.array([[ 663,  553],[ 527,  677],[ 474,  602],[ 604,  492]])
INT_4 = np.array([[ 647,  369],[ 700,  330],[ 590,  214],[ 545,  269]])
INT_5 = np.array([[ 966,  263],[ 909,  210],[ 775,  338],[ 818,  399]])
INT_6 = np.array([[ 897,  490],[ 834,  543],[ 952,  681],[1015,  626]])
INT_7 = np.array([[ 722,  624],[ 596,  765],[ 523,  683],[ 657,  555]])
INT_8 = np.array([[ 594,  430],[ 645,  371],[ 541,  275],[ 489,  340]])
INT_9 = np.array([[   3,  310],[   5,  448],[  64,  462],[  64,  300]])
INT_10 = np.array([[ 160,  202],[ 162,  271],[ 286,  275],[ 292,  206]])
INT_11 = np.array([[1404,  868],[1256,  870],[1260,  791],[1400,  787]])
INT_12 = np.array([[1569,  756],[1569,  620],[1504,  620],[1506,  761]])
INTERSECTIONS = np.array([INT_1,INT_2,INT_3,INT_4,INT_5,INT_6,INT_7,INT_8,INT_9,INT_10,INT_11,INT_12])

#Distance that the car must be from a waypoint in order bump that waypoint off our list.
MIN_DIST = 80
X = 0
Y = 1

class drawWaypoint:
    def __init__(self, im, fig, rad, test):
        self.im = im
        self.fig = fig
        self.rad = rad
        self.cid = fig.canvas.mpl_connect('button_press_event', self)
        self.wayPoints = np.array([])
        self.test = test

    def setWP(self,wp):
        self.wayPoints = wp

    def __call__(self, event):
        if self.test:
            for i in range(len(self.wayPoints)):
                if reachedWP((len(self.im[0,:])-event.xdata,event.ydata),self.wayPoints[i]):
                    print("True")
        else:
            ix = int(event.xdata)
            iy = int(event.ydata)
            ax = self.fig.gca()
            ax.plot(ix,iy,'ro')
            if len(self.wayPoints)==0:
                self.wayPoints = np.array([(len(self.im[0,:])-ix,iy)])
            else:
                self.wayPoints = np.append(self.wayPoints,[(len(self.im[0,:])-ix,iy)],axis=0)
            self.fig.canvas.draw()

    def print(self):
        print(self.wayPoints)

    def writeCSV(self,path):
        a = np.asarray(self.wayPoints)
        np.savetxt(path, a, fmt="%d", delimiter=",")


#can't use ~/. Need to use the actual path.
def setWayPoint(imPath,csvPath):
    imglob = mpimg.imread(imPath)
    rad = 20
    fig = plt.figure()

    wp = drawWaypoint(imglob,fig,rad,False)

    plt.imshow(imglob)
    plt.show()

    wp.print()

    wp.writeCSV(csvPath)

def testWayPoint(imPath,wp):
    imglob = mpimg.imread(imPath)
    rad = 20
    for i in range(len(wp)):
        cv2.circle(imglob, (len(imglob[0,:])-wp[i,0],wp[i,1]), rad, (255, 0, 0), -1)

    fig = plt.figure()

    test = drawWaypoint(imglob,fig,rad,True)

    test.setWP(wp)

    plt.imshow(imglob)
    plt.show()

def csv2WayPoint(csvPath):
    return np.genfromtxt(csvPath,dtype="int",delimiter=",")

def reachedWP(curLoc, wp):
    global MIN_DIST, X, Y
    dist = math.sqrt(((curLoc[X]-wp[X])**2)+(curLoc[Y]-wp[Y])**2)
    return (dist < MIN_DIST)

#this function returns the index of the intersection we are in, or returns -1 if we aren't in any intersection
#An intersection is a 2D array or list with four vertices, so this function needs to be a list of 2D arrays or lists
#curLoc is a tuple
def reachedIntersection(curLoc, intersections):
    for i in range(len(intersections)):
        path = mpltPath.Path(intersections[i])
        if path.contains_point(curLoc):
            return i+1
    return -1

