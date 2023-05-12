import asyncio
from fogverse import Consumer
import cv2
import os
from dotenv import load_dotenv
from fogverse.logging import CsvLogging
import uuid

class MyClient(CsvLogging, Consumer):
    def __init__(self, loop=None):
      self.topic_pattern = os.getenv('TOPIC_PATTERN', '')
      self.consumer_conf = {
        'group_id': str(uuid.uuid4())
      }
      CsvLogging.__init__(self)
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
