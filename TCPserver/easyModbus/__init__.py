
def combine_byte(byte_hi, byte_lo): # combine two bytes to a 16-bit integer
    if(byte_hi > 0xff or byte_lo > 0xff):
        raise ValueError('Exceeds the randge of an 8-bit byte')
    return (byte_hi << 8) | byte_lo

def decom_int(num): # big endian
    if(num > 0xffff):
        raise ValueError('Exceeds the range of a 16-bit integer')
    return [num >> 8, num & 0xff]


def checkInput(f): # Decorator, used to verify the input list
    def wrapper(*args, **kwargs):
        if(len(args[0]) == 0):
            raise ValueError('Empty list!')
        return f(*args, **kwargs)
    return wrapper

@checkInput
def get_CRC(data): # accept a list of integers (hex). Returns a pair of CRC verification code (for Modbus-RTU protocol)
    xor_const = 0xA001 # xor constant defined by the Modbus RTU protocol
    crc_reg = 0xFFFF # Initialize the register to b11111111
    
    # calculating CRC
    for i in range(0, len(data)):
        crc_reg ^= data[i]
        # eight rounds of shift and xor
        for j in range(8):
            #crc_reg >>= 1 # shift the register to right for 1 digit
            if(crc_reg & 0x0001): # judge if the shifted's last digit is 1
                crc_reg >>= 1
                crc_reg ^= xor_const
            else:
                crc_reg >>= 1
    return bytearray([crc_reg & 0xFF, crc_reg >> 8])

@checkInput
def append_CRC(data):
    crc = get_CRC(data)
    return data + crc

@checkInput
def isValid_CRC(data):
    crc = get_CRC(data[0:-2])
    return crc == data[-2:]

@checkInput
def get_LRC(): # accept a list of integers (hex). Returns a single byte of LRC verification code ()
    return