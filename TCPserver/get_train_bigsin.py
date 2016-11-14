# the TCP server for the DTU serverices

import signal
import sys
import socket  
import time
import psycopg2
import datetime
import easyModbus as mb
from TCPconfig import *

NUM_OF_SENSORS = 5 # maximum number of sensors
name_table = ''

def SIGINT_handler(signum, frame): # do some clean up when being Interrupted
    global isSIGINT
    isSIGINT = True
    print("Process terminated!\n")

## database
# global conn
def init_db(): # initialize the database
    global conn
    conn = psycopg2.connect(host="localhost", database="ve450", user=db_owner, password=db_passwd)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE %s (time varchar, mot_temp real, room_temp real, current real, displacement real, processing int);"%name_table)
        print("Table %s created\n"%name_table)
    except:
        print("Table %s exists, skipped\n"%name_table)
    conn.commit()
    cursor.close()
    return # placeholder

def write_db(phy_data): # log the sensor readings in the database
    now = datetime.datetime.now()
    str_time = datetime.datetime.strftime(now, '%Y-%m-%d|%H:%M:%S:%f')
    write_data = tuple([str_time] + phy_data[0:5])
    cursor = conn.cursor()
    str_table = 'INSERT INTO %s '%name_table
    cursor.execute(str_table + "values (%s, %s, %s, %s, %s, %s)", write_data)
    print('Wrote to the database', write_data)
    conn.commit()
    cursor.close()
    return # placeholder

def convert_to_phy(reg_data): # convert the direct register readings to real physical quantities 
    phy_data = [0] * NUM_OF_SENSORS
    # sensor 1 motor temperature (celsus)
    phy_data[0] = (reg_data[0] / 400 - 4) / (20 - 4) * 200 + 0
    # sensor 2 room temerature (celsus)
    phy_data[1] = (reg_data[1] / 400 - 4) / (20 - 4) * 200 + 0
    # sensor 3 current (mA)
    phy_data[2] = (reg_data[2] / 400 - 4) / (20 - 4) * 5000 + 0
    # sensor 4 displacement (mm)
    phy_data[3] = (reg_data[3] / 400 - 4) / (20 - 4) * 125 - 1.9
    # sensor 5
    phy_data[4] = int(reg_data[5] > 2000)
    return phy_data


# MODBUS command, read register 1
# command_read = [
#                 [0xfe, 0x04, 0, 0, 0, 0x01, 0x25, 0xc5], # read register 1
#                 [0xfe, 0x04, 0, 1, 0, 0x01, 0x74, 0x05], # read register 2
#                 [0xfe, 0x04, 0, 2, 0, 0x01, 0x84, 0x05], # read register 3
#                 [0xfe, 0x04, 0, 3, 0, 0x01, 0xd5, 0xc5], # read register 4
#                 [0xfe, 0x04, 0, 4, 0, 0x01, 0x64, 0x04], # read register 5
#                 [0xfe, 0x04, 0, 5, 0, 0x01, 0x35, 0xc4], # read register 6
#                 [0xfe, 0x04, 0, 6, 0, 0x01, 0xc5, 0xc4], # read register 7
#                 [0xfe, 0x04, 0, 7, 0, 0x01, 0x94, 0x04]] # read register 8

# the MODBUS command that reads analog in on IPAM3402 platform
command_read = bytearray([0xaa, 0x04, 0x00, 0x40, 0x00, 0x08]) # No CRC appended!
# A typical response
# [ADDR, FUNC, COUNT , REG0, REG0, REG1, REG1, ..., REGN, REGN, CRC, CRC]
# REG0: MOT_TEMP, REG1: ROOM_TEMP, REG2: CURRENT, REG3: DISPLACEMENT, REG4: VOID, REG5: IN_PROCESS
# The adress of the server, as well as the port number
address = (host_address, port_DTU)

ra = []

signal.signal(signal.SIGINT, SIGINT_handler)
isSIGINT = False
#######################################################################################
##                                    Main body                                      ## 
#######################################################################################
if __name__ == '__main__':
    name_table = input('name of table: ')
    socket.setdefaulttimeout(timeout)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
    s.bind(address) 
    init_db() # initialize the database
    while(not isSIGINT):
        isValidConn = False
        while(not isValidConn and not isSIGINT):
            # Initiate a TCP server process
            while(not isSIGINT):
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
            try:
                print('sending verification request\n')
                ss.sendall(mb.append_CRC(command_read))
            except:
                print('Write error\n')
                continue

            try:
                ra = ss.recv(512)
                print(list(map(lambda x:hex(x), ra)))
            except:
                print('Read timeout\n')
                ss.close()
                isValidConn = False
                continue
            if(ra[0] == command_read[0]):
                isValidConn = True
                break 
        time.sleep(0.5)
        ####################### Connection verified ###########################
        print('connection verified!\n')
        reg_data = [0] * 8 # store sensor readings received
        while(not isSIGINT):      
            time.sleep(0.02)                  
            try:
                print('sending read request\n')
                ss.sendall(mb.append_CRC(command_read))
            except:
                print('send failed!\n')
                break

            try:
                ra = ss.recv(512)
            except:
                print('read timeout\n')
                continue
            
            print(list(map(lambda x:hex(x), ra)))

            # extract analog quantities
            if(mb.isValid_CRC(ra)):
                count_of_reg = ra[2] >> 1
                for i in range(count_of_reg):
                    reg_data[i] = mb.combine_byte(ra[(i<<1) + 3], ra[(i<<1) + 4])
                write_db(convert_to_phy(reg_data)) # write data to the database
                print('written data:', reg_data)
            else:
                print("CRC verification mismatch\n")
                continue

    try:
        ss.close()
    except:  
        print("connection already closed\n")
    s.close()
    conn.close() 
    sys.exit() 
    print("Bye~\n")