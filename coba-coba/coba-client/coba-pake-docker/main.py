import asyncio
from fogverse import Consumer
import cv2

class MyConsumer(Consumer):
    def __init__(self, loop=None):
      self.siapa = "consumer"
      # === UNTUK TANPA DOCKER ===
      self.consumer_servers = "localhost:9093"
      self.consumer_topic = "result"
      # ======
      Consumer.__init__(self, loop=loop)
    
    def process(self, data):
      cv2.imshow("Image", data)
      cv2.waitKey(1)
      return data
  
    async def send(self, data):
      pass

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
