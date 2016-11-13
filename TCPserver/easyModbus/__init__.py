__all__ = ['encoder']

def combine_byte(byte_hi, byte_lo): # combine two bytes to a 16-bit integer
    if(byte_hi > 0xff or byte_lo > 0xff):
        raise ValueError('Exceeds the randge of an 8-bit byte')
    return (byte_hi << 8) | byte_lo

def decom_int(num): # big endian
    if(num > 0xffff):
        raise ValueError('Exceeds the range of a 16-bit integer')
    return [num >> 8, num & 0xff]
