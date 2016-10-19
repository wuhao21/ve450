import numpy
import time
import re,sys
import string
import signal
from socket import *

def quit(signum, frame):
    print('Stopping the generator...')
    tcpCliSock.close()
    sys.exit()

signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)
HOST = '59.78.35.20' 
#HOST = '127.0.0.1'
PORT = 8002 
BUFSIZ = 1024
ADDR = (HOST, PORT)

sensorNum = 4

tcpCliSock = socket(AF_INET, SOCK_STREAM) 
tcpCliSock.connect(ADDR) 

while True:
    rlist = list(numpy.random.random(size = sensorNum))
    data = ','.join(str(i) for i in rlist)
    print(data)
    tcpCliSock.send(data.encode("UTF-8")) # 向服务器传输数据
    time.sleep(2)


tcpCliSock.close()
