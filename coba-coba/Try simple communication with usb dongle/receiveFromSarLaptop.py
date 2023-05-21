import socket

localIP     = ""
localPort   = 9096
bufferSize  = 65527

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

while True:
    data, addr = UDPServerSocket.recvfrom(bufferSize)

    print("Data: ", data)
    print("Addr: ", addr)