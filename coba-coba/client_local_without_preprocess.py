import asyncio
from fogverse import Consumer, ConsumerStorage
import cv2

class MyConsumer(Consumer, ConsumerStorage):
    def __init__(self, loop=None):
      self.siapa = "consumer"
      self.consumer_topic = "input"
      self.consumer_servers = "localhost:9093"
      Consumer.__init__(self, loop=loop)
      ConsumerStorage.__init__(self)
    
    def process(self, data):
      cv2.imshow("Image", data)
      cv2.waitKey(1)
      return data

async def main():
  consumer = MyConsumer()
  tasks = [consumer.run()]
  try:
    await asyncio.gather(*tasks)
  except:
    for t in tasks:
      t.close()

if __name__ == '__main__':
  asyncio.run(main())
