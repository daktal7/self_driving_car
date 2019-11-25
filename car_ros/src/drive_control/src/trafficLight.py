import cv2
from roadDetect import roadDetect as rd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

RED_LOWER = 0
RED_UPPER = 40
GREEN_CENTER = 60
GREEN_BUFFER = 20
GREEN_LOWER = GREEN_CENTER-GREEN_BUFFER
GREEN_UPPER = GREEN_CENTER+GREEN_BUFFER+10
SAT_CUTOFF = 150

#box is given as two vertices. It is an array of form [x1, y1, x2, y2]
#first point must be upper left had corner and second point is lower right
#the image is given in BGR
#returns 'r' for red and 'g' for green

#commented out stuff is for debugging
def detectLight(im,box,colorFormat):
    resRed = 0
    resGreen = 0
    #light = np.zeros((box[2]-box[0],box[3]-box[1],3),np.uint16)
    for i in range(box[0],box[2]):
        for j in range(box[1],box[3]):
            hsvPix = cv2.cvtColor(np.array([[im[j, i]]]),colorFormat) #YOU MAY NEED TO SWITCH THE J AND THE I
            #light[i - box[0], j - box[1]] = hsvPix
            if RED_LOWER <= (hsvPix[0,0,0]+20)%180 <= RED_UPPER and hsvPix[0,0,1] > SAT_CUTOFF:
                resRed = resRed + 1
                #light[i - box[0], j - box[1],0] = 255
            if GREEN_LOWER <= hsvPix[0,0,0] <= GREEN_UPPER and hsvPix[0,0,1] > SAT_CUTOFF:
                resGreen = resGreen + 1
                #light[i - box[0], j - box[1], 1] = 255
    #print("resRed", resRed)
    #print("resGreen", resGreen)
    if resGreen > resRed:
        return 'g'
    return 'r'
    #return light