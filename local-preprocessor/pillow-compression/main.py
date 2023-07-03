import asyncio
import cv2

from fogverse import Consumer, Producer, ConsumerStorage
from fogverse.logging.logging import CsvLogging

from io import BytesIO
from PIL import Image
import numpy as np

class LocalPreprocessorStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class LocalPreprocessor(CsvLogging, Producer):
    def __init__(self, consumer):
        self.consumer = consumer
        CsvLogging.__init__(self)
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, bbytes):
        buffer = BytesIO(bbytes)
        compressed_image = Image.open(buffer)
        data = np.array(compressed_image)
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
