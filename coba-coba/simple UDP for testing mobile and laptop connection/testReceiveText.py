import socket

localIP     = "127.0.0.1"
localPort   = 8090
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
 
# Set up reply message
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Listen for incoming datagrams
while(True):
    message, address = UDPServerSocket.recvfrom(bufferSize)

    print("Message from Client:{}".format(message))
    print("Client IP Address:{}".format(address))

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)