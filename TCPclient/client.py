from socket import *

HOST = '59.78.35.20' #由于服务器开设在自己电脑上，所以主机是本地
PORT = 8002 #同一个连接端口
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM) #同样的TCP套接字
tcpCliSock.connect(ADDR) # 连接相应的地址，初始化TCP服务器的连接

while True:
    data = input('> ')
    if not data:
        break
    tcpCliSock.send(data.encode("UTF-8")) # 向服务器传输数据
    if not data:
        break


tcpCliSock.close()
