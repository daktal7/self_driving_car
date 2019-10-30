import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from roadDetect import roadDetect as rd


# things to fix:
# merge the lines
# find the region of interest automatically
# reduce noise to get better curved line performance
x1 = 0
y1 = 1
x2 = 2
y2 = 3


# just does some basic math
def find_intersection(line_1,line_2):
    slope_1 = classic_slope(line_1)
    slope_2 = classic_slope(line_2)
    if slope_2 == None or slope_1 == None:
        return None
    if slope_1==slope_2:
        return None
    x = ((slope_2*line_2[x2])-(slope_1*line_1[x2])+line_1[y2]-line_2[y2])/(slope_2-slope_1)
    y = slope_1*(x-line_1[x1])+line_1[y1]

    return np.array([x,y])


def classic_slope(line):
    return (line[y2]-line[y1])/(line[x2]-line[x1])

# straight vanishing point [1183.76185021  711.03806387]

def print_image(im):
    im_hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    plt.figure()
    plt.imshow(im)

    plt.figure("gray")
    plt.imshow(im_gray,cmap="gray")

    plt.figure("hue")
    plt.imshow(im_hsv[:,:,0],cmap="gray")

    plt.figure("saturation")
    plt.imshow(im_hsv[:, :, 1], cmap="gray")

    plt.figure("brightness")
    plt.imshow(im_hsv[:, :, 2], cmap="gray")

    plt.show()


# detect the whole image if preline is none or there was no line detected
if __name__ == "__main__":
    RESIZEX = 640
    RESIZEY = 480
    reg = 3.5 # used to define the general region of interest, the image will be blacked out from 0 to reg/10 along y
    #stpClose = cv2.resize(mpimg.imread('images/stoplight_close.jpg'),(RESIZEX,RESIZEY))
    #stpClose_can = rd.getCanny(stpClose)

    #stpClose_msk = rd.region_of_interest(stpClose_can,
     #                                 np.array([
      #                                    [0, len(stpClose_can[:,0])],
       #                                   [0, int((reg*len(stpClose_can[:,0]))//10)],
        #                                  [len(stpClose_can[0,:]), int((reg*len(stpClose_can[:,0]))//10)],
         #                                 [len(stpClose_can[0,:]), len(stpClose_can[:,0])]
          #                             ])
           #                           )
   # stpFar = cv2.resize(mpimg.imread('images/stoplight_far.jpg'),(RESIZEX,RESIZEY))
    stpsgnClose = cv2.resize(mpimg.imread('stopsign_far.jpg'),(RESIZEX,RESIZEY))
    stpsgnClose_can = rd.getCanny(stpsgnClose)
    #stpsgnFar = cv2.resize(mpimg.imread('images/stopsign_far.jpg'),(RESIZEX,RESIZEY))

    stpsgnClose_msk = rd.region_of_interest(stpsgnClose_can,
                                      np.array([
                                          [0, len(stpsgnClose_can[:,0])],
                                          [0, int((reg*len(stpsgnClose_can[:,0]))//10)],
                                          [len(stpsgnClose_can[0,:]), int((reg*len(stpsgnClose_can[:,0]))//10)],
                                          [len(stpsgnClose_can[0,:]), len(stpsgnClose_can[:,0])]
                                       ])
                                      )

    plt.figure()
    plt.imshow(stpsgnClose_hsv[:,:,1],cmap='gray')

    #plt.figure()
    #plt.imshow(stpClose_msk,cmap='gray')

    #interLines = rd.detectIntersection(stpClose_msk,1,None,None)

    #line_im = rd.draw_lines(stpClose, interLines, [255, 0, 0])

    #plt.figure()
    #plt.imshow(line_im)

    plt.show()


if __name__ == "__notmain__":
    # Straight road
    image = mpimg.imread('images/road_1.jpeg')

    #These were used to create the region of interest. I just manually figured out which points to choose.
    v1 = [890,len(image[:,0,0])]
    v2 = [len(image[0, :, 0]), len(image[:, 0, 0])]
    v3 = [len(image[0,:,0]),1480]
    v4 = [1610,860]
    v5 = [1154, 860]
    vertices = np.array([v1,v2,v3,v4,v5])

    # convert to grayscale.
    gray_im = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #masked_gray = region_of_interest(gray_im, vertices)

    #plt.figure()
    #plt.imshow(masked_gray,cmap="gray")

    can_im = cv2.Canny(gray_im, 200, 240)

    masked_can = rd.region_of_interest(can_im, vertices)

    # a single line is represented as an array of size four, [x1,y1,x2,y2]
    # the split image method
    s_lines = rd.split_detect(masked_can,10,0,len(masked_can[0,:]))
    # not using the split image method
    lines = cv2.HoughLinesP(masked_can, rho=6, theta=np.pi / 60, threshold=300, lines=np.array([]), minLineLength=100, maxLineGap=400)

    line_st_1 = lines[0,0,:]
    m_line_st_1 = (rd.get_slope(line_st_1))-90

    other_found = False

    n = 0
    while not other_found:
        m_temp = rd.get_slope(lines[n,0,:])-90
        if m_temp is not None and m_temp*m_line_st_1 < 0:
            other_found = True
        else:
            n = n+1

    # calculate the vanishing point
    vp_st = find_intersection(line_st_1, lines[n,0,:])

    print("straight vanishing point",vp_st)

    line_im = rd.draw_lines(image,lines,[255,0,0])
    line_sp = rd.draw_lines(image, s_lines, [255, 0, 0])

    plt.figure("houghlines")
    plt.imshow(line_im)

    plt.figure("splitlines")
    plt.imshow(line_sp)

    #plt.show()

    #curved road
    curved_im = mpimg.imread('images/curved_road.jpg')
    v1_c = [0,len(curved_im[:,0,0])]
    v2_c = [len(curved_im[0, :, 0]), len(curved_im[:, 0, 0])]
    v3_c = [len(curved_im[0,:,0]),1035]
    v4_c = [1095,513]
    v5_c = [1145, 253]
    v6_c = [812,222]
    v7_c = [483,323]
    v8_c = [162,605]
    vertices = np.array([v1_c,v2_c,v3_c,v4_c,v5_c,v6_c,v7_c,v8_c])#,np.array([v1,v2,v4]),np.array([v3,v5,v6])]

    #plt.figure()
    #plt.imshow(curved_im)

    curved_gray = cv2.cvtColor(curved_im, cv2.COLOR_BGR2GRAY)
    #masked_gray_c = region_of_interest(curved_gray, vertices)

    #plt.figure()
    #plt.imshow(masked_gray,cmap="gray")

    can_im = cv2.Canny(curved_gray, 230, 240)
    masked_can_c = rd.region_of_interest(can_im, vertices)

    lines_c = rd.split_detect(masked_can_c,10,0,len(masked_can_c[0,:]))

    vp_c = find_intersection(lines_c[7, 0, :], lines_c[1, 0, :])
    print("curved vanishing point", vp_c)

    plt.figure()
    plt.imshow(masked_can_c,cmap="gray")

    #lines_c = cv2.HoughLinesP(masked_can_c, rho=6, theta=np.pi / 60, threshold=300, lines=np.array([]), minLineLength=100,
                            #maxLineGap=400)

    line_im_c = rd.draw_lines(curved_im, lines_c,[255,0,0])

    plt.figure()
    plt.imshow(line_im_c)

    plt.show()

    line_im_c = rd.draw_lines(curved_im, lines_c,[255,0,0])
    print("done")
