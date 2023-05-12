import asyncio
from fogverse import Consumer
import cv2
from dotenv import load_dotenv
import uuid

class MyClient(Consumer):
    def __init__(self, loop=None):
      self.consumer_conf = {
        'group_id': str(uuid.uuid4())
      }
      Consumer.__init__(self, loop=loop)

    def process(self, data):
      cv2.imshow("Final Image", data)
      cv2.waitKey(1)
      return data
  
    def encode(self, data):
      pass

    async def send(self, data):
      pass

async def main():
  consumer = MyClient()
  tasks = [consumer.run()]
  try:
    await asyncio.gather(*tasks)
  except:
    for t in tasks:
      t.close()

if __name__ == '__main__':
  load_dotenv()
  asyncio.run(main())
