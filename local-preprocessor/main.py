import asyncio
import cv2
import os

from fogverse import Consumer, Producer, ConsumerStorage
from fogverse.logging.logging import CsvLogging

class LocalPreprocessorStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class LocalPreprocessor(CsvLogging, Producer):
    def __init__(self, consumer):
        self.consumer = consumer
        log_filename = f"logs/log_{self.__class__.__name__}_with_cloud_{os.getenv('UAV_COUNT')}_uav_attempt_{os.getenv('ATTEMPT')}.csv"
        CsvLogging.__init__(self, filename=log_filename)
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self,data):
        img_resized = cv2.resize(data, (480,640))
        return cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

async def main():
    consumer = LocalPreprocessorStorage()
    producer = LocalPreprocessor(consumer)
    tasks = [consumer.run(), producer.run()]
    try:
        await asyncio.gather(*tasks)
    except:
        for t in tasks:
            t.close()

if __name__ == '__main__':
    asyncio.run(main())
