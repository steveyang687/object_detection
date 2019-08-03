# 导入socket模块
import socket



def sendfn(x, y, z, classnum,conn):

    sendstr = "PQ"+str(x)+","+str(y)+","+str(z)+","+str(classnum)
    #sendstr = "PQ5,1,2,3,4,5,4"
    conn.send(sendstr.encode('utf-8'))
    print(sendstr)
# waiting for feedback,receive twice: 0 is Robot has receivedd data \ 1 is Robot has catched box and droped pharmacy
    #for i in range(2):
    recedata = conn.recv(1024)
    print("From Robot Client: "+str(recedata))
    conn.send(sendstr.encode('utf-8'))

if __name__ == '__main__':
    while True:
        sendfn(1,2,3,4)