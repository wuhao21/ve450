import socket
address = ('23.83.239.12', 8899)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)