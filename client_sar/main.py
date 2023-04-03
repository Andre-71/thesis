# ======================================================================
# Versi pakai ConsumerStorage
# -> Udah versi terbaik sejauh ini

import asyncio
from fogverse import Producer, AbstractConsumer, ConsumerStorage
import cv2
from djitellopy import tello
from fogverse.util import get_timestamp_str

class DroneConstumer(AbstractConsumer):
  def __init__(self, loop=None, executor=None):
    self._loop = loop or asyncio.get_event_loop()
    self._executor = executor
    self.consumer = tello.Tello()
  
  def start_consumer(self):
    self.consumer.connect()
    self.consumer.streamon()

  def _receive(self):
    return self.consumer.get_frame_read().frame

  async def receive(self):
    return await self._loop.run_in_executor(self._executor, self._receive)
  
  def process(self, data):
    cv2.imshow("Image", data)
    cv2.waitKey(1)
    return data

  def close_consumer(self):
    self.consumer.streamoff()
    self.consumer.end()

class MyStorage(ConsumerStorage, DroneConstumer):
  def __init__(self):
    self.siapa = "consumer"
    self.frame_size = (640, 480)
    ConsumerStorage.__init__(self)
    DroneConstumer.__init__(self)
  
  def process(self, data):
    data = super().process(data)
    data = cv2.resize(data, self.frame_size)
    return data

class MyProducer(Producer):
  def __init__(self, consumer):
    self.siapa = "producer"
    self.producer_topic = "input"
    self.producer_servers = "localhost:9093"
    self.consumer = consumer
    Producer.__init__(self)

  async def receive(self):
    return await self.consumer.get()

async def main():
  consumer = MyStorage()
  # producer = MyProducer(consumer=consumer)
  tasks = [consumer.run()]
  try:
    await asyncio.gather(*tasks)
  except:
    for t in tasks:
      t.close()

if __name__ == '__main__':
  asyncio.run(main())

# ======================================================================
# Versi ga pakai ConsumerStorage 
# -> Udah versi terbaik sejauh ini
# -> Setelah sadar kalo ConsumerStorage penting untuk menjaga barangkali producer sedang ada masalah,
# -> namun consumer baiknya tetep jalan, ternyata ini ga kepake lagi.

# import asyncio
# from fogverse import Producer, AbstractConsumer
# import cv2
# from djitellopy import tello
# from fogverse.util import get_timestamp_str

# class DroneConsumer(AbstractConsumer):
#   def __init__(self, loop=None, executor=None):
#     self._loop = loop or asyncio.get_event_loop()
#     self._executor = executor
#     self.consumer = tello.Tello()
  
#   def start_consumer(self):
#     self.consumer.connect()
#     self.consumer.streamon()

#   def _receive(self):
#     return self.consumer.get_frame_read().frame

#   async def receive(self):
#     return await self._loop.run_in_executor(self._executor, self._receive)

#   def process(self, data):
#     cv2.imshow("Image", data)
#     cv2.waitKey(1)
#     return data

#   def close_consumer(self):
#     self.consumer.streamoff()
#     self.consumer.end()

# class MyProducer(DroneConsumer, Producer):
#   def __init__(self, loop=None):
#     self.siapa = "producer"
#     self.producer_topic = "input"
#     self.producer_servers = "localhost:9093"
#     self.frame_idx = 1
#     DroneConsumer.__init__(self, loop=loop)
#     Producer.__init__(self, loop=loop)
  
#   def process(self, data):
#     data = super().process(data)
#     scale_percent = 71
#     width = int(data.shape[1] * scale_percent / 100)
#     height = int(data.shape[0] * scale_percent / 100)
#     dim = (width, height)
#     return cv2.resize(data, dim)
  
#   async def send(self, data):
#     key = str(self.frame_idx).encode()
#     headers = [
#       ('timestamp', get_timestamp_str().encode())
#     ]
#     await super().send(data, key=key, headers=headers)
#     self.frame_idx += 1

# async def main():
#   producer = MyProducer()
#   tasks = [producer.run()]
#   try:
#     await asyncio.gather(*tasks)
#   except:
#     for t in tasks:
#       t.close()

# if __name__ == '__main__':
#   asyncio.run(main())