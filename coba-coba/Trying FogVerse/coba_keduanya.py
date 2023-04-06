import asyncio
from fogverse import Producer, Consumer

class TestProducer(Producer):
    def __init__(self):
        self.producer_topic = "test"
        self.producer_servers = "localhost:9093"
        self.counter = 50
        Producer.__init__(self)

    async def receive(self):
        await asyncio.sleep(500/1000)
        self.counter += 1
        returnedString = "Halo " + self.counter.__str__()
        return bytes(returnedString, 'utf-8')

class TestConsumer(Consumer):
    def __init__(self):
        self.consumer_topic = "test"
        self.consumer_servers = "localhost:9093"
        Consumer.__init__(self)

    async def send(self, data):
        print(data)
        return data

async def main():
    producer = TestProducer()
    consumer = TestConsumer()
    tasks = [producer.run(), consumer.run()]
    try:
        await asyncio.gather(*tasks)
    finally:
        for t in tasks:
            t.close()

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(main())
#     finally:
#         loop.close()

if __name__ == '__main__':
  asyncio.run(main())