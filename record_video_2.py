#record_video.py
# USAGE: python3 record_video.py --output output/my_output.avi

# import the necessary packages
import argparse
import imutils
import cv2

FPS = 30
print("beginning recording")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help = "path to output video")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help = "minimum probability to filter weak detections")
ap.add_argument("-t","--time",type=int,default=10, help="time to record the video")
args = vars(ap.parse_args())	

Standard_video = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L) # ls -ltr /dev/video*
Depth_video = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L)
writer = None
writer_depth = None
(W, H) = (None, None)

for i in range(args["time"]*FPS):
    # read the next frame from the file
    (grabbed, frame) = Standard_video.read()
    (grabbed_depth, frame_depth) = Depth_video.read()
 
    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed or not grabbed_depth:
        break

    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # check if the video writer is None
    if writer is None:
        # initialize our video writer
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter("Standard_video.avi", fourcc, 30,(frame.shape[1], frame.shape[0]), True)
        writer_depth = cv2.VideoWriter("Depth_video.avi", fourcc, 30,(frame_depth.shape[1], frame_depth.shape[0]), True)
 
    # write the output frame to disk
    writer.write(frame)
    writer_depth.write(frame_depth)

writer.release()
writer_depth.release()
Standard_video.release()
Depth_video.release()
