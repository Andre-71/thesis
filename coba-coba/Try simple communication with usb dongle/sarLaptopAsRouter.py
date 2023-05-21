import socket

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = ("192.168.137.1", 9011)
bufferSize = 65527

UDPClientSocket.sendto("halo", serverAddressPort)