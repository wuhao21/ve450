# the TCP server for the DTU serverices

import signal
import sys
import socket  
import time
import psycopg2
import datetime
from TCPconfig import *

def SIGINT_handler(signum, frame): # do some clean up when being Interrupted
    global isSIGINT
    isSIGINT = True
    print("Process terminated!\n")

def combine_byte(byte_hi, byte_lo): # combine two bytes to a 16-bit integer
    return (byte_hi << 8) | byte_lo

## database
# global conn
def init_db(): # initialize the database
    global conn
    conn = psycopg2.connect(host="localhost", database="ve450", user=db_owner, password=db_passwd)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE CNCLinear (time varchar, room_temp real, mot_temp real, current real, displacement real);")
    except:
        print("Table CNCLinear exists, skipped\n")
    conn.commit()
    cursor.close()
    return # placeholder

def write_db(phy_data): # log the sensor readings in the database
    now = datetime.datetime.now()
    str_time = datetime.datetime.strftime(now, '%Y-%m-%d|%H:%M:%S:%f')
    write_data = tuple([str_time] + phy_data[0:4])
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CNCLinear values (%s, %s, %s, %s, %s)", write_data)
    print('Wrote to the database', write_data)
    conn.commit()
    cursor.close()
    return # placeholder

def convert_to_phy(reg_data): # convert the direct register readings to real physical quantities 
    phy_data = reg_data.copy()
    # sensor 1 room temperature (celsus)
    phy_data[0] = phy_data[0] / 65535 * 200 + 0
    # sensor 2 motor temerature (celsus)
    phy_data[1] = phy_data[1] / 65535 * 200 + 0
    # sensor 3 current (mA)
    phy_data[2] = phy_data[2] / 65535 * 10000 + 0
    # sensor 4 displacement (mm)
    phy_data[3] = phy_data[3] / 65535 * 200
    return phy_data

NUM_OF_SENSORS = 8 # maximum number of sensors

# MODBUS command, read register 1
command_read = [
                [0xfe, 0x04, 0, 0, 0, 0x01, 0x25, 0xc5], # read register 1
                [0xfe, 0x04, 0, 1, 0, 0x01, 0x74, 0x05], # read register 2
                [0xfe, 0x04, 0, 2, 0, 0x01, 0x84, 0x05], # read register 3
                [0xfe, 0x04, 0, 3, 0, 0x01, 0xd5, 0xc5], # read register 4
                [0xfe, 0x04, 0, 4, 0, 0x01, 0x64, 0x04], # read register 5
                [0xfe, 0x04, 0, 5, 0, 0x01, 0x35, 0xc4], # read register 6
                [0xfe, 0x04, 0, 6, 0, 0x01, 0xc5, 0xc4], # read register 7
                [0xfe, 0x04, 0, 7, 0, 0x01, 0x94, 0x04]] # read register 8

# The adress of the server, as well as the port number
address = (host_address, port_DTU)

ra = []

signal.signal(signal.SIGINT, SIGINT_handler)
isSIGINT = False
#######################################################################################
##                                    Main body                                      ## 
#######################################################################################
if __name__ == '__main__':
    socket.setdefaulttimeout(timeout)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
    s.bind(address) 
    init_db() # initialize the database
    while(not isSIGINT):
        isValidConn = False
        while(not isValidConn and not isSIGINT):
            # Initiate a TCP server process
            while(True):
                print('Waiting for connections...')
                try:
                    s.listen(5)  
                    ss, addr = s.accept() 
                except:
                    print("Listen timeout\n")
                else:
                    break
            print(['got connected from', addr])

            # Judge if the connection is from DTU
            time.sleep(0.5)
            ss.send(bytearray(command_read[0]))
            try:
                ra = ss.recv(512)
                print(list(map(lambda x:hex(x), ra)))
            except:
                print('Read timeout\n')
                ss.close()
                isValidConn = False
                continue

            if(ra[0] == 0xfe):
                isValidConn = True
            else:
                ss.close() # close the current connection and wait for the next one

        while(isValidConn and not isSIGINT):
            time.sleep(0.5)
            reg_data = [0] * NUM_OF_SENSORS # store the recived sensor reading
            for i in range(0, NUM_OF_SENSORS):
                if(isSIGINT):
                    break
                print('Reading from sensor %d\n'%i)
                ss.send(bytearray(command_read[i]))
                try:
                    ra = ss.recv(512)      
                    print(list(map(lambda x:hex(x), ra)))    
                except:
                    print('Read timeout\n')
                    isValidConn = False # terminate the connection
                    break 
                reg_data[i] = combine_byte(ra[3], ra[4]) # the range of value is from 0 to 65535
            if(isValidConn): # store the readings in the database only if the connection was valid till end         
                write_db(convert_to_phy(reg_data)) # write data to the database

    ss.close()  
    s.close()
    conn.close() 
    sys.exit() 
    print("Bye~\n")