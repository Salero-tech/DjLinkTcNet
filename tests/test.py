import socket
from tcnet.data.message import message
UDP_IP = ""
UDP_PORT = 60000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print(message(data, addr))

# https://www.tc-supply.com/_files/ugd/b1c714_0b351a4099c14e738f0cd7fcea623265.pdf