import serial
import time
from gcode_config import *
lst_gcode = [
    'G21', # MM UNIT
    'G92', # set origin
    'G90', # absolute location
    'START',
    'G01 X10000 F3000'
    'G28', # go to the origin
    'END'
]
if __name__ == '__main__':
    comm = serial.Serial(comm_port, 19200)
    #comm.open()
    time.sleep(5)
    comm.readline()
    comm.read_all()
    print('serial port ready\n')
    for i in range(50):
        print('runnning round %d\n'%i)
        comm.read_all()
        for gcode in lst_gcode:
            print(gcode)
            comm.write(bytearray(gcode.encode('UTF-8')))
            comm.write(b'\r\n')
            ra = comm.readline()
            print(ra)
            time.sleep(0.2)
        time.sleep(5)
        
