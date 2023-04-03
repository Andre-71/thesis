import asyncio
from fogverse import Producer

class TestProducer(Producer):
    def __init__(self):
        self.siapa = "producer"
        self.producer_topic = "test"
        self.producer_servers = "localhost:9093"
        self.counter = 100
        Producer.__init__(self)

    async def receive(self):
        await asyncio.sleep(500/1000)
        self.counter += 1
        returnedString = "Halo " + self.counter.__str__()
        return bytes(returnedString, 'utf-8')

async def main():
    producer = TestProducer()
    tasks = [producer.run()]
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
