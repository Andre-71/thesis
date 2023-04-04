import asyncio
import torch
import os

from fogverse import Consumer, Producer, ConsumerStorage

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        self.siapa = "consumer"
        self.consumer_topic = os.getenv('CONSUMER_TOPIC', [])
        self.consumer_servers = os.getenv('CONSUMER_SERVERS', "")
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyInferncer(Producer):
    def __init__(self, consumer):
        self.siapa = "producer"
        MODEL = os.getenv('MODEL', 'yolov5n')
        self.model = torch.hub.load('ultralytics/yolov5', MODEL)
        self.producer_topic = os.getenv('PRODUCER_TOPIC', "")
        self.producer_servers = os.getenv('PRODUCER_SERVERS', "")
        self.consumer = consumer
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        results = self.model(data)
        print(results)
        return results.render()[0]

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)


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
