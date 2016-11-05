import socket
import select

from TCPconfig import *
address = (host_address, port_phone)
#socket.setdefaulttimeout(5)
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(True)
    isConnected = False
    while(not isConnected):
        try:
            s.connect(address)
        except:
            print('Connection failed\n')
        else:
            print('Connection established\n')
            isConnected = True
    while(True):
            ra = s.recv(512)
            if(ra != b''):
                s.sendall(b'ack\n')
                print(ra)
            else:
                print('disconnected\n')
                break
            
    

    