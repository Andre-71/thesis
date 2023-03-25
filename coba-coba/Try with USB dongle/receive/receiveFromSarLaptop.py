# import socket
# import numpy as np
# import cv2
# import numpy as np
# import os
# from io import BytesIO

# localIP     = ""
# localPort   = 9011
# bufferSize  = 65527

# # Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Bind to address and ip
# UDPServerSocket.bind((localIP, localPort))

# print("UDP server up and listening")

# while(True):
#     # imgFile, address = UDPServerSocket.recvfrom(bufferSize)
#     # print("Client IP Address:{}".format(addr))

#     data, addr = UDPServerSocket.recvfrom(bufferSize)
#     frame_file = open("frame.npz", 'wb')
#     while(data):
#         frame_file.write(data)
#         data, addr = UDPServerSocket.recvfrom(bufferSize)
    
#     img = np.load("frame.npz")
#     os.remove("frame.npz")

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

# CARA 2
# data, addr = UDPServerSocket.recvfrom(bufferSize)
# print("Client address: ", addr)
# frame_file = open("frame.npz", 'wb')

# # while(data):
# #     frame_file.write(data)
# #     data, addr = UDPServerSocket.recvfrom(bufferSize)
# #     print("Client address: ", addr)
    
# frame_file.write(data)
# frame_file.close()

# loaded = np.load("frame.npz")

# cv2.imshow("Image", loaded["frame"])
# cv2.waitKey(1)

# # os.remove("frame.npz")

# Final
import socket
import numpy as np
import cv2
import numpy as np
from io import BytesIO

localIP     = ""
localPort   = 9011
bufferSize  = 65527

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

while True:
    data, addr = UDPServerSocket.recvfrom(bufferSize)
    print("Client address: ", addr)

    loaded = np.load(BytesIO(data))

    cv2.imshow("Image", loaded["frame"])
    cv2.waitKey(1)