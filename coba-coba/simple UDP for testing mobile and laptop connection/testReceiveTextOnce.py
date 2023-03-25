import socket

localIP     = ""
localPort   = 9011
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.settimeout(15.0)
try:
  # Bind to address and ip
  UDPServerSocket.bind((localIP, localPort))
  
  print("UDP server up and listening")
    
  # Set up reply message
  msgFromServer       = "Hello UDP Client"
  bytesToSend         = str.encode(msgFromServer)
  
  # Listen for incoming datagrams
  message, address = UDPServerSocket.recvfrom(bufferSize)
  
  print("Message from Client:{}".format(message))
  print("Client IP Address:{}".format(address))
  
  # Sending a reply to client
  UDPServerSocket.sendto(bytesToSend, address)
  
  UDPServerSocket.close()
except socket.timeout:
  UDPServerSocket.close()
  print("Server kelamaan ga ada request masuk")