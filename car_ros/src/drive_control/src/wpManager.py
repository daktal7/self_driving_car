#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import matplotlib.path as mpltPath

#this are the coordinates for all the intersections
#SI_1 = np.array([[342,776],[296,821],[401,929],[444,880]])
SI_1 = np.array([[350,969],[255,874],[333,794],[425,889]])
#SI_2 = np.array([[492,880],[541,931],[653,825],[602,778]])
SI_2 = np.array([[523,894],[622,803],[683,866],[586,959]])
#SI_3 = np.array([[598,724],[494,620],[541,561],[653,675]])
SI_3 = np.array([[521,598],[608,699],[681,628],[576,541]])
#SI_4 = np.array([[440,624],[391,575],[289,679],[340,723]])
SI_4 = np.array([[253,633],[350,540],[443,627],[348,726]])  
SI_5 = np.array([[384,133],[386,2],[287,5],[293,145]])
SI_6 = np.array([[277,141],[125,143],[123,226],[279,222]])
SI_7 = np.array([[777,1432],[941,1430],[947,1349],[777,1359]])
#SI_8 = np.array([[779,1442],[696,1430],[689,1576],[781,1580]])  was too far foreward
SI_8 = np.array([[759,1442],[676,1430],[669,1576],[761,1580]]) #lowered all x values by 20
STOP_INTERSECTIONS = np.array([SI_1,SI_2,SI_3,SI_4,SI_5,SI_6,SI_7,SI_8])
#These are the warning intersections
WI_1 = np.array([[328,786],[209,911],[310,1025],[432,889]])
WI_2 = np.array([[505,887],[636,1027],[748,927],[612,790]])
WI_3 = np.array([[604,713],[758,561],[634,452],[503,609]])
WI_4 = np.array([[318,491],[462,635],[362,737],[190,585]])
WI_5 = np.array([[300,140],[484,138],[490,2],[294,2]])
WI_6 = np.array([[134,158],[278,148],[272,324],[134,332]])
WI_7 = np.array([[782,1407],[938,1405],[940,1225],[788,1229]])
WI_8 = np.array([[570,1582],[574,1429],[777,1424],[780,1584]])
WARNING_INTERSECTIONS = np.array([WI_1,WI_2,WI_3,WI_4,WI_5,WI_6,WI_7,WI_8])

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
def reachedWarningIntersection(curLoc):
    global WARNING_INTERSECTIONS
    for i in range(len(WARNING_INTERSECTIONS)):
        path = mpltPath.Path(WARNING_INTERSECTIONS[i])
        if path.contains_point(curLoc):
            return i+1
    return -1


#this function returns the index of the intersection we are in, or returns -1 if we aren't in any intersection
#An intersection is a 2D array or list with four vertices, so this function needs to be a list of 2D arrays or lists
#curLoc is a tuple
def reachedStopIntersection(curLoc):
    global STOP_INTERSECTIONS
    for i in range(len(STOP_INTERSECTIONS)):
        path = mpltPath.Path(STOP_INTERSECTIONS[i])
        if path.contains_point(curLoc):
            return i+1
    return -1

