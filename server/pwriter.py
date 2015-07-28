import socket
import sys
import os 
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util import Counter
import subprocess
#ctr = Counter.new(128)
#obj = AES.new('This is a key456', AES.MODE_CTR,counter=ctr)
#obj2 = AES.new('This is a key457', AES.MODE_CTR,counter=ctr)
HOST = ''   
PORT = 9000 
 

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
#print 'Socket bind complete'
def filewriter(addr,count,portseq,userdata,sensor_no,actuator_no,algo_no):
  o=0
  portnos=sensor_no+actuator_no
  t=1
  fo = open("robot%d.py"%count, "w")
  p=[]
  ps=[]
  pa=[]
  t=portseq
  for q in range(int(portnos)): 
      portseq=t+q
      p.append(portseq) 
  fo.write("import socket \nimport sys\nimport xlwt\nfrom xlwt import Workbook\nfrom tempfile import TemporaryFile\n\n\n")
  if algo_no == '1': 
    fo.write("import facedetect\n")
  elif algo_no=='2':
    fo.write("import hsvdetect\n")   
  for y in range(int(sensor_no)):
    fo.write("###############################################################################\n\n") 
    fo.write("host%d=''\n" %y)
    fo.write("port%d=%d\n\n"%(y,p[y]))
    fo.write("try:\n  s%d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n"%y);
    fo.write("except socket.error, msg%d :\n"%y)
    fo.write("  print 'Failed to create socket. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n"%(y,y))
    fo.write("try:\n");
    fo.write("  s%d.bind((host%d, port%d))\n"%(y,y,y))
    fo.write("except socket.error, msg%d :\n"%y)
    fo.write("  print 'Bind failed. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n\n\n"%(y,y))
    #fo.write("d%d = s%d.recvfrom(6144)\nsensordata%d = d%d[0]\nsensoraddr%d = d%d[1]\n\n\n"%(y,y,y,y,y,y))
    ps.append(p[y])
  for y in range(int(actuator_no)):
    r=y+sensor_nos
    fo.write("###############################################################################\n\n") 
    fo.write("host%d=''\n" %r)
    fo.write("port%d=%d\n\n"%(r,p[r]))
    fo.write("try:\n  a%d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n"%r);
    fo.write("except socket.error, msg%d :\n"%r)
    fo.write("  print 'Failed to create socket. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n"%(r,r))
    fo.write("try:\n");
    fo.write("  a%d.bind((host%d, port%d))\n"%(r,r,r))
    fo.write("except socket.error, msg%d :\n"%r)
    fo.write("  print 'Bind failed. Error Code : ' + str(msg%d[0]) + ' Message ' + msg%d[1]\n  sys.exit()\n\n\n"%(r,r))
    pa.append(p[r])
  #fo.write("book = Workbook()\n")
  #fo.write("sheet1 = book.add_sheet('Sheet 1')\n")
  #fo.write("j=1\n")
  for y in range(int(actuator_no)):
    r=y+sensor_nos
    fo.write("d%d = a%d.recvfrom(6144)\nrobotack%d = d%d[0]\nrobotaddr%d = d%d[1]\n\n\n"%(r,r,r,r,r,r))
    #pa.append(p[r])
  rat=10 
  #print 'sensor portlist',ps
  #print 'actuatorportlist',pa
  #for y in range(int(sensor_no)):
    #fo.write("sheet1.write(0,%d,'SensorData %d')\n"%(y,y))  
  fo.write("while 1:\n")
  for y in range(int(sensor_no)):
    fo.write("  d%d = s%d.recvfrom(6144)\n  sensordata%d = d%d[0]\n  sensoraddr%d = d%d[1]\n"%(y,y,y,y,y,y))
    #fo.write("  sheet1.write(j,%d,sensordata%d)\n"%(y,y))
    #fo.write("  sheet1.col(%d).width = 10000\n"%y) 
    #fo.write("  print 'cloud : received sensor data %d'\n\n\n"%y)
  #fo.write("  j=j+1\n")
  fo.write("  x=2\n")
  if algo_no == '1':
    fo.write("  facedata=facedetect.facedetect(sensordata0)\n")
  elif algo_no== '2':
    fo.write("  pixeldata=hsvdetect.hsvdetect(sensordata0)\n") 
  fo.write("  y=str(x)\n\n")
  if algo_no == '1':
    o=1
  elif algo_no =='2':
    o=2
  for r in range(int(actuator_no)):
    y=r+sensor_nos
    #fo.write("  print 'cloud : sending actuator data %d'\n"%y)
    if o==1:
      fo.write("  a%d.sendto(facedata,robotaddr%d)\n"%(y,y))
      o=0
    elif o==2:
      fo.write("  a%d.sendto(pixeldata,robotaddr%d)\n"%(y,y))
      o=0
    else:
      fo.write("  a%d.sendto(y,robotaddr%d)\n"%(y,y))
  #fo.write("  book.save('robot%d.xls')\n"%count)
  #fo.write("  book.save(TemporaryFile())\n") 
  fo.close
  #msg='A file named as robot%d.py has been generated! \n'%count
  #s.sendto(msg, addr)
  recentportval=portseq
  return ps,pa,p,recentportval
count=0
sensorportlist=[]
actuatorportlist=[] 
robotlist=[]
details=[]
portseq =50000 
def status(ps,count):          
  x=0  
while 1:
    print "Hello There! I am the Master Server and I am waiting for your command" 
    d = s.recvfrom(2048)
    dat = d[0]
    addr = d[1]
    if not dat: 
        break
    ctr = Counter.new(128)
    obj = AES.new('This is a key456', AES.MODE_CTR,counter=ctr)
    data=obj.decrypt(dat)
    print data
    if data=='addrobot':
      count=count+1
      dat = s.recvfrom(1024)
      userdat = dat[0]
      addr = dat[1]
      userdata=obj.decrypt(userdat)
      sensor_nos=int(userdata)
      dat = s.recvfrom(1024)
      userdat = dat[0] 
      addr = dat[1]
      userdata=obj.decrypt(userdat)
      actuator_nos=int(userdata)
      dat = s.recvfrom(1024)
      userdat = dat[0] 
      addr = dat[1]
      userdata=obj.decrypt(userdat)
      algo=userdata
      dat = s.recvfrom(1024)
      userdat = dat[0] 
      addr = dat[1]
      userdata=obj.decrypt(userdat)
      algo_no=userdata
      #print userdata
      ps,pa,p,recentportval=filewriter(addr,count,portseq,userdata,sensor_nos,actuator_nos,algo_no)
      subprocess.Popen("python robot%d.py"%count, stdout=subprocess.PIPE,shell=True)
      #os.system("gnome-terminal -e 'bash -c \"python robot%d.py &; exec bash\"'"%count)
      #ack='ack'
      #s.sendto(ack, addr)
      m1=str(count)
      s.sendto(m1, addr)
      for i in range(len(ps)):
        s.sendto(str(ps[i]),addr)     
      for i in range(len(pa)):
        s.sendto(str(pa[i]),addr)  
      portseq=recentportval+1
      
    elif data=='status':
      if count == 0:
        msg='No Robots have been added'
        s.sendto(msg,addr) 
      else:
        status(ps,count) 
        msg='Number of robots created : ' +str(count)     
        s.sendto(msg,addr)
        #for i in range(count):
         # msg='List of ports used for sensors of Robot %d : '%i +  str(sensorportlist[i]) +'List of ports used for sensors of Robot %d :'%i + str(actuatorportlist[i]) 
         
    else:
        #print data
        msg='Please Enter a valid command!'      
        s.sendto(msg,addr)       
s.close()
