import asyncio
import torch
import os
import datetime

from fogverse import Consumer, Producer, ConsumerStorage
from fogverse.logging.logging import BaseLogging

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        self.siapa = "consumer"
        # === HANYA UNTUK CEK TANPA DOCKER ===
        # self.consumer_servers="localhost:9093"
        # self.consumer_topic="input"
        # ======
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyInferncer(Producer):
    def __init__(self, consumer):
        self.siapa = "producer"
        # === HANYA UNTUK CEK TANPA DOCKER ===
        # self.producer_servers = "localhost:9093"
        # self.producer_topic = "result"
        # ======
        MODEL = os.getenv('MODEL', 'yolov5n')
        self.model = torch.hub.load('ultralytics/yolov5', MODEL)
        self.consumer = consumer
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        results = self.model(data)
        return results.render()[0]

    async def process(self, data):
        now = datetime.datetime.now()
        print("WAKTU SEBELUM PROCESS: " + str(now.time()))
        process_result = await self._loop.run_in_executor(None,
                                               self._process,
                                               data)
        now = datetime.datetime.now()
        print("WAKTU SETELAH PROCESS: " + str(now.time()))
        return process_result


async def main():
    consumer = MyStorage()
    producer = MyInferncer(consumer)
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
