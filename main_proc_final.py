from research.object_detection import object_detection_tutorial as obj
from research import cameratest as cam
import numpy as np
import time
import socket


def sendfn(x, y, z, classnum,conn):

    sendstr = "PQ"+str(x)+","+str(y)+","+str(z)+","+str(classnum)+","
    #sendstr = "PQ5,1,2,3,4,5,4"
    conn.send(sendstr.encode('utf-8'))
    print(sendstr)
    recedata = conn.recv(1024)
    print("From Robot Client: "+str(recedata))

def detect():
    cam.pyloncapt()

    x, y, classnum, boxnum, index, score = obj.obj_det()

    print("识别的东西：")
    print(x)
    print(y)
    classify = 0
    z = np.zeros(boxnum)
    i=index
    ysend = (42.997+37.4/2-37.4*y[i])*10  # 根据几何关系得到，自行修改
    ysend = round(ysend,3)
    xsend = (10.280+31.28/2-31.28*x[i])*10
    xsend = round(xsend,3)
    score = score[i]
    classnum = classnum[i]
    print("classnum is: "+str(classnum))
    if (classnum==1 or classnum ==2 or classnum ==3 or classnum ==4 or classnum ==5):
        classify = 3 #可回收
        print("可回收垃圾")
    elif(classnum==6 or classnum ==7 or classnum ==8):
        classify = 2  # 有害
        print("有害垃圾")
    elif(classnum==9 or classnum ==10 ):
        classify = 4  # 湿
        print("湿垃圾")
    elif (classnum == 11 or classnum == 12):
        classify = 4  # 干
        print("干垃圾")
    else:
        input() #当前无垃圾
    #print("score is" +str(score))
    h=0
    z[i]=h+160
    z[i]= round(z[i],3)
    #z=10

    print("x coordinate is: " + str(xsend))
    print("y coordinate is: " + str(ysend))
    print("z coordinate is: " + str(z[i]))
    print("classification is:" + str(classify))
    print("score is:"+ str(score))
    return xsend,ysend,z[i],classify,score

print('This is PC server')
ip_port = ("192.168.8.100", 8080)
#print("A")
skt = socket.socket()
#print("A")
#print("A")
skt.bind(ip_port)
skt.listen()
connect, addr = skt.accept()
emm='steve'
connect.send(emm.encode('utf-8'))
# recedata1 = connect.recv(1024)
# print("!!!!"+str(recedata1))

while True:
    print("into loop")
    x, y, z,classify, score = detect()
    print(score)
    if(score >= 0.70): # 当且仅当识别的可信度超过70%才抓取
        sendfn(y-20, -x-18, z-5, classify, connect)  #-20 -18是手动修正值
        #time.sleep(40)


        print("waiting")
        finished = connect.recv(1024)
        #print("received")
        print("signal received:")
        print(str(finished))
        if str(finished) == "b'ok'":
            finished = "cleared"
        else:
            time.sleep(30)
        #print("00")

skt.close()
