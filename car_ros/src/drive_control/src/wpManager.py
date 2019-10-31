#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import matplotlib.path as mpltPath


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
def reachedIntersection(curLoc, intersections):
    for i in range(len(intersections)):
        path = mpltPath.Path(intersections[i])
        if path.contains_point(curLoc):
            return i
    return -1

