import asyncio
import torch

from fogverse import Consumer, Producer, ConsumerStorage

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        self.siapa = "consumer"
        self.consumer_topic = ['input']
        self.consumer_servers = "localhost:9093"
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyInferncer(Producer):
    def __init__(self, consumer):
        self.siapa = "producer"
        MODEL = "yolov5n"
        self.model = torch.hub.load('ultralytics/yolov5', MODEL, force_reload=True)
        self.producer_topic = "result"
        self.producer_servers = "localhost:9093"
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
