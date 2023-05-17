import asyncio
from fogverse import Consumer

class TestConsumer(Consumer):
    def __init__(self):
        self.siapa = "consumer"
        self.consumer_topic = "test"
        self.consumer_servers = "localhost:9094"
        Consumer.__init__(self)

    async def send(self, data):
        print(data)
        return data

async def main():
    consumer = TestConsumer()
    tasks = [consumer.run()]
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
