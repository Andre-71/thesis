from scapy.all import sniff, hexdump, raw
from PIL import Image
import os
# import binascii
# import cv2

def filter_video_frame(frame):
    return frame.dport == 11111

def print_video_frame_receiver_port(frame):
    return hexdump(frame)
    # return frame.load
    # return Raw(frame)
    # return binascii.hexlify(bytes(frame.load))

# while True:
  # packet = sniff(count=20, lfilter=filter_video_frame, prn=print_video_frame_receiver_port)

# while True:
  # packet = sniff(count=1, lfilter=filter_video_frame, prn=print_video_frame_receiver_port)
  # img = cv2.resize(frame.load, (360, 240))
  # cv2.imshow("Image", img)
  # cv2.waitKey(1)

packet = sniff(count=1, lfilter=filter_video_frame)
image_in_bytes = raw(packet[0])
print(image_in_bytes)
result_file = 'result_file'
with open(result_file, 'wb') as file_handler:
    file_handler.write(image_in_bytes)
# Image.open(result_file).save(result_file + '.png', 'PNG')
# os.remove(result_file)
