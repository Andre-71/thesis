import asyncio
import torch
import os

from fogverse import Consumer, Producer, ConsumerStorage
from fogverse.logging.logging import CsvLogging
from fogverse.util import get_header, numpy_to_base64_url

from PIL import Image
from io import BytesIO
import numpy as np
import cv2

class LocalInferencerStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class LocalInferencer(CsvLogging, Producer):
    def __init__(self, consumer):
        model =  os.getenv('MODEL', 'yolov5n')
        self.model = torch.hub.load('ultralytics/yolov5', model)
        self.model.classes = [0]
        self.consumer = consumer
        CsvLogging.__init__(self)
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, bbytes):
        buffer = BytesIO(bbytes)
        compressed_image = Image.open(buffer)
        compressed_image_array = np.array(compressed_image)
        data = cv2.resize(compressed_image_array, (640, 480), interpolation=cv2.INTER_LANCZOS4)
        results = self.model(data)
        return results.render()[0]

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

    def encode(self, img):
        return numpy_to_base64_url(img, os.getenv('ENCODING', 'jpg')).encode()
    
    async def send(self, data):
        headers = list(self.message.headers)
        headers.append(('type',b'final'))
        await super().send(data, headers=headers)

# ======================================================================
class LocalInferencer1(LocalInferencer):
    def __init__(self, consumer):
        super().__init__(consumer)

    async def send(self, data):
        headers = list(self.message.headers)
        uav_id = get_header(headers, 'uav')
        headers.append(('from',b'local_inferencer'))
        self.message.headers = headers
        self.producer_topic = f'final_{uav_id}'
        await super().send(data)
# ======================================================================
class LocalInferencer2(LocalInferencer):
    def __init__(self, consumer):
        self.producer_topic = 'result'
        super().__init__(consumer)

ARCHITECTURES = {
    "only_local": (LocalInferencerStorage, LocalInferencer1),
    "with_cloud": (LocalInferencerStorage, LocalInferencer2),
}

async def main():
    architeture = os.getenv('ARCHITECTURE', "with_cloud")
    _Consumer, _Producer = ARCHITECTURES[architeture]
    consumer = _Consumer()
    producer = _Producer(consumer)
    tasks = [consumer.run(), producer.run()]
    try:
        await asyncio.gather(*tasks)
    finally:
        for t in tasks:
            t.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
