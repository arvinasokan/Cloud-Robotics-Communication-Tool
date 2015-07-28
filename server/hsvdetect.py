import numpy as np
import cv2.cv as cv
import cv2


newx = 320
newy = 240
nx = 320
ny = 240
def hsvdetect(dat):
    n=0
    c=0
    d = np.fromstring(dat,dtype='uint8')
    img=cv2.imdecode(d,cv2.CV_LOAD_IMAGE_COLOR)
    #img=cv2.resize(img,(640,480))
    img = cv2.blur(img,(10,10))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([100,40,40], dtype=np.uint8)
    upper = np.array([120,200,200], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    #cv2.imshow('mask',mask)
    contours,hierarchy = cv2.findContours (mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    cx=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
            n=1
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        #else:
            #n=0
    #if(n==1):
      #M = cv2.moments(best_cnt)
      #cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    #else:
      #cx=0
    pixels=[cx,cy]
    r=bytearray(pixels)
    cv2.waitKey(5)
    return r

