import signal
import sys
import socket  
import time
import datetime
from TCPconfig import *

global isSIGINT
def SIGINT_handler(signum, frame): # do some clean up when being Interrupted
    global isSIGINT
    isSIGINT = True
    print("Process terminated!\n")

signal.signal(signal.SIGINT, SIGINT_handler)
isSIGINT = False
# The adress of the server, as well as the port number
address = (host_address, port_phone)
ra = []
json_str = b'{"temperature":"30.03","displacement":"123.33","current":"321","wave":"triangle","temp_high":"0","current_high":"0"}\n'
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
                  ss.send(bytearray(json_str))
                  print('sent\nWaiting for acknowledgemen\n');
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
                  time.sleep(2)
                

    try:
        ss.close()
    except:
        print("socket serverice not created\n")

    s.close()
    sys.exit()
    print("Bye\b")
        