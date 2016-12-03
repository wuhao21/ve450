import signal
import sys
import socket
import time
import datetime
import psycopg2
from TCPconfig import *


global s,ss


global isSIGINT
def SIGINT_handler(signum, frame): # do some clean up when being Interrupted
     global isSIGINT
     isSIGINT = True
     try:
       ss.close()
     except:
       print('socket not yet connected!\n')
     s.close()
     print("Process terminated!\n")
     sys.exit()


def read_db(): # read the database
    global conn
    global records
    conn = psycopg2.connect(host="localhost", dbname="ve450", user="root", password="1234") #database configuration
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM CNCLinear_result") #table name
        records = cursor.fetchall()
    except:
        print("Table is not find\n")
    conn.commit()
    cursor.close()
    return

signal.signal(signal.SIGINT, SIGINT_handler)
isSIGINT = False
# The adress of the server, as well as the port number
address = (host_address, port_phone)
ra = []
if __name__ == '__main__':
     socket.setdefaulttimeout(10)
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
     s.bind(address)
     while(not isSIGINT):
         while(not isSIGINT):
             print('Waiting for connections...')
             try:
                 s.listen(5)
                 ss, addr = s.accept()
             except:
                 print("Listen timeout\n")
             else:
                 print(['got connected from', addr])
                 time.sleep(0.5)
                 while(not isSIGINT):
                   read_db();
                   json_str = '{"time":"'+str(records[-1][0])+'","temperature":"'+str(round(records[-1][1],1))+'","displacement":"'+str(round(records[-1][4],1))+'","current":"'+ str(round(records[-1][3],1))+'","wave":"'+str(records[-1][5])+ '","temp_high":"'+str(records[-1][6])+'","current_high":"'+str(records[-1][7])+'","block":"'+str(records[-1][8])+'","process":"digging","count":"'+str(records[-1][9])+'"}\n'
                   print(json_str)
                   ss.send(json_str.encode('utf-8'))

                   print('sent\nWaiting for acknowledgemen\n');
                   '''
                   try:
                     ra = ss.recv(512)
                   except:
                     print('read timeout\n')
                   else:
                     if(ra != b''):
                       print('ack\n')
                     else:
                       print('disconnected\n')
                       break
                   '''


     try:
         ss.close()
     except:
         print("socket serverice not created\n")

     s.close()
     sys.exit()
     print("Bye\b")
