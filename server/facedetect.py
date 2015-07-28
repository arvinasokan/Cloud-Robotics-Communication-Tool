import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def facedetect(y):
  d = np.fromstring(y,dtype='uint8')
  img = np.zeros((320,240,3), np.uint8)
  img=cv2.imdecode(d,cv2.CV_LOAD_IMAGE_COLOR)
  img2=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  faces = face_cascade.detectMultiScale(img2, 1.3, 5)
  #cv2.imshow('image',img)
  #print faces
  #k = cv2.waitKey(5) & 0xFF
  r=bytearray(faces)
  return r
cv2.destroyAllWindows()
