from socket import *
from time import ctime
import time
import psycopg2
import psycopg2.extras
import pprint
import datetime
##HOST = '127.0.0.1'
HOST = '59.78.35.20'  # 主机
PORT = 8002 # 端口号，可以随意选择
BUFSIZ = 1024
ADDR = (HOST, PORT) #主机端口号组成一个套接字地址
tcpSerSock = socket(AF_INET, SOCK_STREAM) #创建一个套接字对象，是AF_INET族的tcp套接字
tcpSerSock.bind(ADDR) #这个函数用于绑定地址到套接字
tcpSerSock.listen(5) # 服务器开始监听连接，参数表示最多允许同时有几个连接进来
threads = []

##全部输出
##conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
##conn = psycopg2.connect(conn_string)
##cursor = conn.cursor()
##cursor.execute("SELECT * FROM linear_position")
##records = cursor.fetchall()
##pprint.pprint(records)

##分行输出
##conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
##conn = psycopg2.connect(conn_string)
##cursor = conn.cursor('name', cursor_factory=psycopg2.extras.DictCursor)
##cursor.execute('SELECT * From linear_position LIMIT 10000')
##
##row_count=0
##for row in cursor:
##    row_count += 1
##    print("row %s %s\n" % (row_count,row))

##创建表
##conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
##conn = psycopg2.connect(conn_string)
##cur = conn.cursor()
##cur.execute('''CREATE TABLE TEST
##       (TIME  timestamp PRIMARY KEY     NOT NULL,
##        SENSOR1 FLOAT    NOT NULL, 
##       SENSOR2  FLOAT    NOT NULL, 
##       SENSOR3  FLOAT    NOT NULL,
##       SENSOR4  FLOAT    NOT NULL);''') 
##print ("Table created successfully") 
## 
##conn.commit() 
##conn.close()

##insert操作
##conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
##conn = psycopg2.connect(conn_string)
##cur = conn.cursor()
## 
##cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )"); 
## 
##cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00 )"); 
## 
##cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )"); 
## 
##cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )"); 
## 
##conn.commit() 
##print ("Records created successfully"); 
##conn.close() 

##select 操作

##conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
##conn = psycopg2.connect(conn_string)
##cur = conn.cursor()
##
##cur.execute("SELECT id, name, address, salary  from COMPANY") 
##rows = cur.fetchall() 
##for row in rows: 
##   print ("ID = ", row[0])
##   print ("NAME = ", row[1]) 
##   print ("ADDRESS = ", row[2]) 
##   print ("SALARY = ", row[3], "\n") 
## 
##print ("Operation done successfully"); 
##conn.close() 


##i=0
##while (i<9):
##    conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
##    conn = psycopg2.connect(conn_string)
##    cur = conn.cursor()
##    cur.execute("INSERT INTO TEST (TIME,SENSOR1,SENSOR2,SENSOR3) VALUES (%s,%s,%s,%s)",(datetime.datetime.now(),i,i*2,i*3)); 
##    conn.commit() 
##    print ("Records created successfully"); 
##    conn.close()
##    i=i+1
##    time.sleep(1)
##  



while True:
    print ('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept() #用于等待连接的到来
    print ('...connected from:',addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ).decode('utf8') #用于接收从客户端发来的数据 参数代表一次最多接受的数据量，这里为1k
        if not data:
            break
        tmp=data.split(',')
        print(data)
        print(tmp[0])
        print(tmp[1])
        conn_string = "host='localhost' dbname='CNCXYZ' user='postgres' password='siemens'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute("INSERT INTO TEST (TIME,SENSOR1,SENSOR2,SENSOR3,SENSOR4) VALUES (%s,%s,%s,%s,%s)",(datetime.datetime.now(),tmp[0],tmp[1],tmp[2],tmp[3])); 
        conn.commit() 
        print ("Records created successfully"); 
        conn.close()
        

    tcpCliSock.close()

tcpSerSock.close()
