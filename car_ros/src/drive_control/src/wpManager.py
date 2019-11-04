#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import matplotlib.path as mpltPath

#this are the coordinates for all the intersections
INT_1  = np.array([[ 454,  878],[ 395,  822],[ 259,  970],[ 328, 1023]]) #Fixed
INT_2  = np.array([[ 541,  834],[ 671,  952],[ 742,  899],[ 610,  773]]) #Fixed
INT_3  = np.array([[ 553,  663],[ 677,  527],[ 602,  474],[ 492,  604]]) #Fixed
INT_4  = np.array([[ 369,  647],[ 330,  700],[ 214,  590],[ 269,  545]]) #Fixed
INT_5  = np.array([[ 263,  966],[ 210,  909],[ 338,  775],[ 399,  818]]) #Fixed
INT_6  = np.array([[ 490,  897],[ 543,  834],[ 681,  952],[ 626, 1015]]) #Fixed
INT_7  = np.array([[ 624,  722],[ 765,  596],[ 683,  523],[ 555,  657]]) #Fixed
INT_8  = np.array([[ 430,  594],[ 371,  645],[ 275,  541],[ 340,  489]]) #Fixed
INT_9  = np.array([[ 310,    3],[ 448,   5 ],[  462,  64],[ 300,   64]]) #Fixed
INT_10 = np.array([[ 202,  160],[ 271,  162],[ 275,  286],[ 206,  292]]) #Fixed
INT_11 = np.array([[868,  1404],[870,  1256],[791,  1260],[787,  1400]]) #Fixed
INT_12 = np.array([[756,  1569],[620,  1569],[620,  1504],[761,  1506]]) #Fixed
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
                if reachedWP((event.ydata,len(self.im[0,:])-event.xdata),self.wayPoints[i]):
                    print("True")
        else:
            ix = int(event.xdata)
            iy = int(event.ydata)
            ax = self.fig.gca()
            ax.plot(ix,iy,'ro')
            if len(self.wayPoints)==0:
                self.wayPoints = np.array([(iy,len(self.im[0,:])-ix)])
            else:
                self.wayPoints = np.append(self.wayPoints,[(iy,len(self.im[0,:])-ix)],axis=0)
            self.fig.canvas.draw()

    def __print__(self):
        print(self.wayPoints)

    def writeCSV(self,path):
        a = np.asarray(self.wayPoints)
        np.savetxt(path, a, fmt="%d", delimiter=",")


#can't use ~/. Need to use the actual path.
def setWayPoint(imPath,csvPath):
    #Set it with Jace's GUI, save to a CSV, rename to the same CSV, push the CSV,
    #then the car will always pull the right points
    imglob = mpimg.imread(imPath)
    rad = 20
    fig = plt.figure()

    wp = drawWaypoint(imglob,fig,rad,False)

    plt.imshow(imglob)
    plt.show()

    wp.__print__()

    wp.writeCSV(csvPath)
# just for testing to see if this thing works
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

# takes a csv file and returns a np.array
def csv2WayPoint(csvPath):
    return np.genfromtxt(csvPath,dtype="int",delimiter=",")

#check to see if you've reached the waypoint
def reachedWP(curLoc, wp):
    global MIN_DIST, X, Y
    dist = math.sqrt(((curLoc[X]-wp[X])**2)+(curLoc[Y]-wp[Y])**2)
    return (dist < MIN_DIST)

#this function returns the index of the intersection we are in, or returns -1 if we aren't in any intersection
#An intersection is a 2D array or list with four vertices, so this function needs to be a list of 2D arrays or lists
#curLoc is a tuple
def reachedIntersection(curLoc):
    for i in range(len(INTERSECTIONS)):
        path = mpltPath.Path(INTERSECTIONS[i])
        if path.contains_point(curLoc):
            return i+1
    return -1

