# from djitellopy import tello
# import cv2
# import socket
# import pickle

# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# serverAddressPort = ("127.0.0.1", 9011)
# bufferSize = 2048

# drone =  tello.Tello()
# drone.connect()
# drone.streamon()
# print(drone.get_battery())
# loopLimit = 100

# while True:
#     try:
#         img = drone.get_frame_read().frame
#         img = cv2.resize(img, (360, 240))
#         # imgInBytes = pickle.dumps(img)
#         # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
#         # print("Message from Server {}".format(msgFromServer[0]))
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#         imgInBytes = img.tobytes()
#         # print(type(imgInBytes))
#         # if imgInBytes:
#         # print(imgInBytes)
#         UDPClientSocket.sendto(imgInBytes, serverAddressPort)
#         print("setelah send")
#     except Exception as e:
#        pass
       

# drone.streamoff()
# drone.end()
# UDPClientSocket.close()

# from djitellopy import tello
# import cv2
# import socket
# import numpy as np
# import os

# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# serverAddressPort = ("127.0.0.1", 9011)
# bufferSize = 65527

# drone =  tello.Tello()
# drone.connect()
# drone.streamon()
# print(drone.get_battery())
# scale_percent = 20

# # loopLimit = 1

# while True:
#   # if loopLimit == 0:
#   #   break
#   img = drone.get_frame_read().frame
#   if img is not None:
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)
#     width = int(img.shape[1] * scale_percent / 100)
#     height = int(img.shape[0] * scale_percent / 100)
#     dim = (width, height)
#     resized_img = cv2.resize(img, dim)
#     # print(resized_img)
#     np.savez_compressed(file="frame", frame=resized_img)
#     frame_file = open("frame.npz", "rb")
#     data = frame_file.read(bufferSize)
#     UDPClientSocket.sendto(data, serverAddressPort)
#     # while data:
#     #   if UDPClientSocket.sendto(data, serverAddressPort):
#     #     data = frame_file.read(bufferSize)
#     print("Sending a frame completed")
#     frame_file.close()
#     os.remove("frame.npz")
#     # loopLimit -= 1

#     # print(data)

#     # frame_file.close()
#     # os.remove("frame.npz")
#     # loopLimit -= 1

# UDPClientSocket.close()
# drone.streamoff()
# drone.end()

# Final
from djitellopy import tello
import cv2
import socket
import numpy as np
import os

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = ("192.168.137.1", 9011)
bufferSize = 65527

drone =  tello.Tello()
drone.connect()
drone.streamon()
scale_percent = 17

while True:
  img = drone.get_frame_read().frame
  if img is not None:
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img, dim)
    np.savez_compressed(file="frame", frame=resized_img)
    frame_file = open("frame.npz", "rb")
    data = frame_file.read(bufferSize)
    UDPClientSocket.sendto(data, serverAddressPort)
    print("Sending a frame completed")
    frame_file.close()
    os.remove("frame.npz")