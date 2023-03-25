import socket

# Prepare message
msgFromClient = "Halo, ini dari HP"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("192.168.0.224", 9011)
bufferSize = 1024

for i in range(10):
  # Create a UDP socket at client side
  UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  UDPClientSocket.settimeout(1.0)
  
  # Send to server using created UDP socket
  UDPClientSocket.sendto(bytesToSend, serverAddressPort)

  try:
    # Reply from server
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print("Message from Server {}".format(msgFromServer[0]))
  except socket.timeout:
    UDPClientSocket.close()
    print("SOCKET TIMED OUT")