import socket

# Prepare message
msgFromClient = "Halo, ini dari HP"
bytesToSend = str.encode(msgFromClient)
print(type(bytesToSend))
print(bytesToSend)
serverAddressPort = ("127.0.0.1", 9011)
bufferSize = 2048

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(1.0)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# try:
#   # Reply from server
#   msgFromServer = UDPClientSocket.recvfrom(bufferSize)
#   print("Message from Server {}".format(msgFromServer[0]))
# except socket.timeout:
#   UDPClientSocket.close()
#   print("SOCKET TIMED OUT")

UDPClientSocket.close()