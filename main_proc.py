from research.object_detection import object_detection_tutorial as obj
from research import cameratest as cam
import numpy as np
import time
import socket
cam.pyloncapt()
x, y, classnum, boxnum = obj.obj_det()

classify = 0

def sendfn(x, y, z, classnum):

    sendstr = "PQ"+str(x)+","+str(y)+","+str(z)+","+str(classnum)+","
    #sendstr = "PQ5,1,2,3,4,5,4"
    conn.send(sendstr.encode('utf-8'))
    print(sendstr)
# waiting for feedback,receive twice: 0 is Robot has receivedd data \ 1 is Robot has catched box and droped pharmacy
    #for i in range(2):
    recedata = conn.recv(1024)
    print("From Robot Client: "+str(recedata))
    conn.send(sendstr.encode('utf-8'))


z = np.zeros(1)
i=0
xsend = (42.997+45.8/2-45.8*x[i])*10
xsend = round(xsend,3)
ysend = (10.280+38.5/2-38.5*y[i])*10
ysend = round(ysend,3)

print(classnum)
if (classnum==1 or classnum ==2 or classnum ==3 or classnum ==4 or classnum ==5):
    classify = 1 #可回收
elif(classnum==6 or classnum ==7 or classnum ==8):
    classify = 2  # 有害
elif(classnum==9 or classnum ==10 ):
    classify = 3  # 湿
elif (classnum == 11 or classnum == 12):
    classify = 4  # 湿
else:
    input() #当前无垃圾

h=0
z[i]=h+220
z[i]= round(z[i], 3)
#z=10

print(xsend)
print(ysend)
print(z[i])

classnum = 1

print('This is PC server')
ip_port = ("192.168.8.100", 8080)
#print("A")
skt = socket.socket()
#print("A")
#print("A")
skt.bind(ip_port)
skt.listen()
#print("A")
conn, addr = skt.accept()

while True:
    sendfn(xsend, -ysend, 100, classify)  #100是手动调校的高度
    time.sleep(5)
    skt.close()
