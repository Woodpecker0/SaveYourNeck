import numpy as np
import cv2
def nothing(x):
    pass
# Create a black image, a window
img = np.zeros((300,500,3), np.uint8)
cv2.namedWindow('image')
# create trackbars for color change
face_t = cv2.createTrackbar('face max width','image',0,300,nothing)
eyes_t = cv2.createTrackbar('eyes max width','image',0,300,nothing)

# create switch for ON/OFF functionality
switch = '0 : normal \n1 : calibrate with A4 paper'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of four trackbars
    face_d = cv2.getTrackbarPos(face_t,'image')
    eyes_d = cv2.getTrackbarPos(eyes_t,'image')
    s = cv2.getTrackbarPos(switch,'image')
    if s == 1:
        pass

cv2.destroyAllWindows()