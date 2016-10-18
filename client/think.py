from socket import *
from time import ctime
import time
import psycopg2
import psycopg2.extras
import pprint
import datetime

HOST = '59.78.35.20'
PORT = 8002
BUFSIZ = 1024
TIMEOUT = 10.0

def think_request(number_of_records, end_time)
	ADDR = (HOST, PORT)
	tcpCliSock = socket(AF_INET, SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	sock.settimeout(10.0)
	msg = tcpCliSock.recv(BUFSIZ).decode('utf8')
	if msg=='who':
		tcpCliSock.send('algo'.encode("UTF-8"))
		sleep(1)
		request = 'request %s %s'%(number_of_records, end_time)#end_time="YYYY-mm-dd|HH:MM:SS:ffffff"
		data = tcpCliSock.recv(BUFSIZ).decode('utf8')
	else:
		continue;
	tcpCliSock.close()

