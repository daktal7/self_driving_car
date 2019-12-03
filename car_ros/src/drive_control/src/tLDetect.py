import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

# im must be in hsv
#returns 'r' for red and 'g' for green
#if box is none the algorithm will run over the entire image
#commented out stuff used for debugging
def isGreen(im):
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

def getNumBlack(im):
    res = 0
    for i in range(len(im[:,0])):
        for j in range(len(im[0,:])):
            if im[i,j] < BLACK_THRESH:
                res = res+1
    return res

def getBox(im,bins,maxI,dx):
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
    return im[0:int(ROI*len(hsvIm[:,0])),(maxI-iLeft)*dx:(maxI+iRight)*dx,:]

#im must be hsv, res is how many cross sections are made
#will return numpy array that contains just the traffic light
def getTL(im):
    bins = np.zeros((RES,2))
    dx = len(im[0,:])//RES
    maxVal = 0
    maxI = -1
    for i in range(RES):
        bins[i,0] = i
        bins[i,1] = getNumBlack(im[0:int(ROI*len(hsvIm[:,0])),i*dx:i*dx+dx,2])
        if bins[i,1] > maxVal:
            maxVal = bins[i,1]
            maxI = i
    return getBox(im,bins,maxI,dx)


im = mpimg.imread("images/leehi_tl1.jpg")

hsvIm = cv2.cvtColor(im,cv2.COLOR_RGB2HSV)

light = getTL(hsvIm)
print(isGreen(light))
roi = 170/len(hsvIm[:,0])

plt.figure()

plt.imshow(im)

plt.figure()
plt.imshow(cv2.cvtColor(light,cv2.COLOR_HSV2RGB))

plt.show()