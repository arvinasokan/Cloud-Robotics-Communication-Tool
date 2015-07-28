import socket   
import sys  
import subprocess
import os 
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util import Counter
#ctr = Counter.new(128)
#obj = AES.new('This is a key456', AES.MODE_CTR,counter=ctr)
#obj2 = AES.new('This is a key457', AES.MODE_CTR,counter=ctr)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
host ='localhost'
#host = raw_input('enter the ip address of the server : ')
#host = '104.131.172.175';
#host = '192.168.81.142';
port = 9000;
userdata=[] 
ipaddr=host
def filewriter(ps_nos,pa_nos,robot_no,ipaddr,algo_no):
  o=0
  fo = open("robot0%d.py"%robot_no, "w")
  fo.write("import socket \nimport sys\n\n\n")
  if algo_no == '1' or algo_no == '2':
    fo.write("import videostream\n\n")
  fo.write("ip_addr='%s'\n"%ipaddr)
  for y in range(len(ps_nos)):
    fo.write("###############################################################################\n\n") 
    fo.write("host%d=''\n" %y)
    fo.write("port%d=%d\n\n"%(y,ps_nos[y]))
    fo.write("try:\n  s%d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n"%y);
    fo.write("except socket.error, msg%d :\n"%y)
    fo.write("  print 'Failed to create socket. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n"%(y,y))
    #fo.write("try:\n");
    #fo.write("  s%d.bind((host%d, port%d))\n"%(y,y,y))
    #fo.write("except socket.error, msg%d :\n"%y)
    #fo.write("  print 'Bind failed. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n\n\n"%(y,y))
    
  for y in range(len(pa_nos)):
    r=len(ps_nos)+y
    fo.write("###############################################################################\n\n") 
    fo.write("host%d=''\n" %r)
    fo.write("port%d=%d\n\n"%(r,pa_nos[y]))
    fo.write("try:\n  a%d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n"%r);
    fo.write("except socket.error, msg%d :\n"%r)
    fo.write("  print 'Failed to create socket. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n"%(r,r))
    #fo.write("try:\n");
    #fo.write("  a%d.bind((host%d, port%d))\n"%(r,r,r))
    #fo.write("except socket.error, msg%d :\n"%r)
    #fo.write("  print 'Bind failed. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n\n\n"%(r,r))
    #fo.write("d%d = a%d.recvfrom(6144)\nrobotack%d = d%d[0]\nrobotaddr%d = d%d[1]\n\n\n"%(r,r,r,r,r,r)) 
  for r in range(len(pa_nos)):
    y=r+len(ps_nos)
    fo.write("print 'sending ack %d'\n"%y)  
    fo.write("a%d.sendto('ack',(ip_addr,%d))\n\n"%(y,pa_nos[r]))
  fo.write("while 1:\n")
  fo.write("  x=1\n")
  if algo_no == '1' or algo_no == '2':
    o=1
  for y in range(len(ps_nos)):
    if o==1:
      fo.write("  y=videostream.videostream()\n")
      fo.write("  s%d.sendto(y,(ip_addr,%d))\n"%(y,ps_nos[y]))
      o=0 
    else:
      fo.write("  s%d.sendto(str(x),(ip_addr,%d))\n"%(y,ps_nos[y]))
    fo.write("  print 'robot : sent sensor data %d'\n"%y)
  if algo_no == '1':
    o=1
  elif algo_no == '2':
    o=2
  else:
    o=0
  for r in range(len(pa_nos)):
    y=r+len(ps_nos)
    if o==1:
      fo.write("  d%d = a%d.recvfrom(6144)\n  actuatordata%d = d%d[0]\n  actuatoraddr%d = d%d[1]\n"%(y,y,y,y,y,y))
    
      fo.write("  videostream.applicationlayer(actuatordata%d)\n"%y)
      o=0
    elif o==2:
      fo.write("  d%d = a%d.recvfrom(6144)\n  actuatordata%d = d%d[0]\n  actuatoraddr%d = d%d[1]\n"%(y,y,y,y,y,y))
    
      fo.write("  videostream.applicationlayer1(actuatordata%d)\n"%y)
      o=0
    elif o==0: 
      fo.write("  d%d = a%d.recvfrom(6144)\n  actuatordata%d = d%d[0]\n  actuatoraddr%d = d%d[1]\n"%(y,y,y,y,y,y))
    fo.write("  print 'robot : received actuator data %d'\n\n\n"%y)
  
     
  fo.close
  
while(1) :
    ps_nos=[]
    pa_nos=[]
    msg = raw_input('Command : ')
    if msg=='addrobot':
      sensor_nos=raw_input('Enter the number of sensors : ')
      actuator_nos=raw_input('Enter the number of actuators : ')
      ipaddr=raw_input('Please enter the ipaddress of your server : ')
      algo=raw_input('Would you like to use any of our built-in algorithm Y / N ? : ')
      #cat=0 
      if algo == 'y':
          algo_no=raw_input('Which of these algorithms would you like to use ? \n 1.FaceDetection(Haars Cascade) \n 2.HSV based Object Detection \n')
      else:
          algo_no=3
      ctr = Counter.new(128)
      obj = AES.new('This is a key456', AES.MODE_CTR,counter=ctr)
      message='addrobot'
      s.sendto(obj.encrypt(message),(host,port))
      s.sendto(obj.encrypt(str(sensor_nos)),(host, port))
      s.sendto(obj.encrypt(str(actuator_nos)),(host,port))
      s.sendto(obj.encrypt(str(algo)),(host,port)) 
      s.sendto(obj.encrypt(str(algo_no)),(host,port)) 
      #d = s.recvfrom(1024)
      #m = d[0]
      #if m=='ack':
      print 'the server file has been generated and deployed!\nGenerating the client module\n'
      d = s.recvfrom(1024)
      robot_no = d[0]
      addr = d[1]
      #robot_no=obj2.decrypt(robot_no)
      print robot_no
      robot_no=int(robot_no)
      for i in range(int(sensor_nos)):  
        d = s.recvfrom(6144)
        m = d[0]
        #m=obj2.decrypt(m)
        m1=int(m)
        ps_nos.append(m1)   
      print ps_nos
      for i in range(int(actuator_nos)):  
        d = s.recvfrom(6144)
        m = d[0]
        #m=obj2.decrypt(m)
        m1=int(m)
        pa_nos.append(m1)
      print pa_nos
      filewriter(ps_nos,pa_nos,robot_no,ipaddr,algo_no)
      #os.system("gnome-terminal -e 'bash -c \"python robot1.py; exec bash\"'")
      os.system("gnome-terminal -e 'bash -c \"python robot0%d.py; exec bash\"'"%robot_no)    
    elif msg =='status':
      s.sendto('status',(host,port)) 
    else: 
      s.sendto('x',(host,port))
