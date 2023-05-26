import asyncio
from fogverse import Producer, AbstractConsumer, ConsumerStorage
import cv2
from djitellopy import tello
from fogverse.logging import CsvLogging
from fogverse.util import get_timestamp_str
import os
from dotenv import load_dotenv
import uuid
from threading import Thread, Event
import keyboard
import psutil
import time
import csv

def drone_controller(drone):
  takeoff_status = False
  while True:
    if takeoff_status == False and keyboard.is_pressed("f"):
      print("f key pressed")
      drone.takeoff()
      takeoff_status = True
    elif takeoff_status == True and keyboard.is_pressed("w"):
      print("w key pressed")
      drone.move_forward(30)
    elif takeoff_status == True and keyboard.is_pressed("s"):
      print("s key pressed")
      drone.move_back(30)
    elif takeoff_status == True and keyboard.is_pressed("a"):
      print("a key pressed")
      drone.move_left(30)
    elif takeoff_status == True and keyboard.is_pressed("d"):
      print("d key pressed")
      drone.move_right(30)
    elif takeoff_status == True and keyboard.is_pressed("l"):
      print("l key pressed")
      drone.rotate_clockwise(30)
    elif takeoff_status == True and keyboard.is_pressed("j"):
      print("j key pressed")
      drone.rotate_counter_clockwise(30)
    elif takeoff_status == True and keyboard.is_pressed("i"):
      print("i key pressed")
      drone.move_up(30)
    elif takeoff_status == True and keyboard.is_pressed("k"):
      print("k key pressed")
      drone.move_down(30)
    elif takeoff_status == True and keyboard.is_pressed("h"):
      print("h key pressed")
      drone.land()
      takeoff_status = False
    else:
      continue

def battery_consumption_logger(event):
  battery_consumption_logger_csvfilename = f"logs/log_sardevice_battery_{os.getenv('ATTEMPT')}.csv"
  with open(battery_consumption_logger_csvfilename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time', 'battery_percentage'])
    while True:
      if event.is_set():
        break
      writer.writerow([get_timestamp_str(), psutil.sensors_battery().percent])
      time.sleep(1)

class DroneFrameConsumer(AbstractConsumer):
  def __init__(self, loop=None, executor=None):
    self._loop = loop or asyncio.get_event_loop()
    self._executor = executor
    self.auto_decode = False
    self.consumer = tello.Tello()
        
  def start_consumer(self):
    self.event = Event()
    Thread(target=battery_consumption_logger, args=(self.event,)).start()
    self.consumer.connect()
    Thread(target=drone_controller, args=(self.consumer, )).start()
    self.consumer.streamon()

  def _receive(self):
    return self.consumer.get_frame_read().frame

  async def receive(self):
    return await self._loop.run_in_executor(self._executor, self._receive)
  
  def process(self, data):
    cv2.imshow("Image from UAV", data)
    cv2.waitKey(1)
    return data

  def close_consumer(self):
    self.event.set()
    self.consumer.streamoff()
    self.consumer.end()

class FrameProducerStorage(DroneFrameConsumer, ConsumerStorage):
  def __init__(self):
    self.frame_size = (640, 480)
    DroneFrameConsumer.__init__(self)
    ConsumerStorage.__init__(self)
  
  def process(self, data):
    data = super().process(data)
    data = cv2.resize(data, self.frame_size)
    return data

class FrameProducer(CsvLogging, Producer):
  def __init__(self, consumer, loop=None):
    self.consumer = consumer
    self.uav_id = f"uav_{os.getenv('UAV_ID', str(uuid.uuid4()))}"
    self.frame_idx = 1
    log_filename = f"logs/log_{self.__class__.__name__}_{os.getenv('SCENARIO', 'with_cloud')}.csv"
    CsvLogging.__init__(self, filename=log_filename)
    Producer.__init__(self, loop=loop)

  async def receive(self):
    return await self.consumer.get()
  
  async def send(self, data):
    key = str(self.frame_idx).encode()
    headers = [
        ('uav', self.uav_id.encode()),
        ('frame', str(self.frame_idx).encode()),
        ('timestamp', get_timestamp_str().encode())]
    await super().send(data, key=key, headers=headers)
    self.frame_idx += 1

async def main():
  consumer = FrameProducerStorage()
  producer = FrameProducer(consumer=consumer)
  tasks = [consumer.run(), producer.run()]
  tasks = [consumer.run()]
  try:
    await asyncio.gather(*tasks)
  except:
    for t in tasks:
      t.close()

if __name__ == '__main__':
  load_dotenv()
  asyncio.run(main())