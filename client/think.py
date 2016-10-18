from socket import *
import time
import psycopg2
import psycopg2.extras
import pprint
import datetime

#HOST = '59.78.35.20'
HOST = '127.0.0.1'
PORT = 8002
BUFSIZ = 1024
TIMEOUT = 10.0

def think_request(number_of_records, end_time):
	ADDR = (HOST, PORT)
	tcpCliSock = socket(AF_INET, SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	tcpCliSock.settimeout(TIMEOUT)
	msg = tcpCliSock.recv(BUFSIZ).decode('utf8')
	if msg=='who':
		tcpCliSock.send('algo'.encode("UTF-8"))
		time.sleep(1)
		request = 'request %d %s'%(number_of_records, end_time)#end_time="YYYY-mm-dd|HH:MM:SS:ffffff"
		tcpCliSock.settimeout(TIMEOUT)
		for _ in range(int(number_of_records)):
			data = tcpCliSock.recv(BUFSIZ).decode('utf8')
		else:
			print('Connected to wrong server.')
	tcpCliSock.close()
	#print(data)

if __name__ == "__main__":
        think_request(10, 'YYYY-mm-dd|HH:MM:SS:ffffff')
