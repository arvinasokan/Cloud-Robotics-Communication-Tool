import numpy as np
import cv2
cap = cv2.VideoCapture(0)
def videostream():
  img = np.zeros((320,240,3), np.uint8)
  ret, img = cap.read() 
  encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),35]
  img2=cv2.resize(img,(320,240))
  if(ret):  
    #img3=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
    #cv2.imshow('image',img3)
    h=0 
  else:
    img3 = np.zeros((320,240,3), np.uint8) 
  retval,imgstr = cv2.imencode('.jpg', img2,encode_param)
  x= bytearray(imgstr)
  y=str(x)
  return y
def applicationlayer(actuatordata):
    img = np.zeros((320,240,3), np.uint8)
    ret, img = cap.read()
    act=np.fromstring(actuatordata,dtype='uint32')
    act1=np.array(act)
    if len(act1) > 3:
      fx=2*act1[0]
      fy=2*act1[1]
      fw=2*act1[2]
      fh=2*act1[3]
      cv2.rectangle(img,(fx,fy),(fx+fw,fy+fh),(0,0,255),2)
    cv2.imshow('i',img)
    cv2.waitKey(5)
def applicationlayer1(actuatordata):
    act=np.fromstring(actuatordata,dtype='uint8')
    #print act[0]
    img = np.zeros((320,240,3), np.uint8)
    ret, img = cap.read()
    cv2.circle(img,(2*act[0],2*act[1]),20,(10,0,255),-1)
    cv2.imshow('image',img)
    cv2.waitKey(5)
    
cv2.destroyAllWindows()

  
