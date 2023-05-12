import asyncio
import torch
import os

from fogverse import Consumer, Producer, ConsumerStorage
from fogverse.logging.logging import CsvLogging
from fogverse.util import get_header

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyLocalInferncer(CsvLogging, Producer):
    def __init__(self, consumer):
        model =  os.getenv('MODEL', 'yolov5n')
        self.model = torch.hub.load('ultralytics/yolov5', model)
        self.consumer = consumer
        CsvLogging.__init__(self)
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        results = self.model(data)
        return results.render()[0]

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

    async def send(self, data):
        headers = list(self.message.headers)
        headers.append(('type',b'final'))
        await super().send(data, headers=headers)

# ======================================================================
class MyLocalInferencerOnlyLocal(MyLocalInferncer):
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
class MyLocalInferencerWithCloud(MyLocalInferncer):
    def __init__(self, consumer):
        self.producer_topic = 'result'
        super().__init__(consumer)

scenarios = {
    "only local": (MyStorage, MyLocalInferencerOnlyLocal),
    "with cloud": (MyStorage, MyLocalInferencerWithCloud),
}

async def main():
    scenario = os.getenv('SCENARIO', "with cloud")
    _Consumer, _Producer = scenarios[scenario]
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
