import asyncio
import uuid
import os

from fogverse import Consumer, Producer
from fogverse.logging import CsvLogging

class LocalForwarder(CsvLogging, Consumer, Producer):
    def __init__(self):
        self.auto_decode = False
        self.auto_encode = False
        CsvLogging.__init__(self)
        Consumer.__init__(self)
        Producer.__init__(self)

# ======================================================================
class LocalForwarder2(LocalForwarder):
    def __init__(self):
        self.consumer_conf = {'group_id': str(uuid.uuid4())}
        super().__init__()

roles = {
    "local2cloud": LocalForwarder,
    "cloud2local": LocalForwarder2,
}

async def main():
    scenario = os.getenv('ROLE')
    _Forwarder = roles[scenario]
    Forwarder = _Forwarder()
    tasks = [Forwarder.run()]
    try:
        await asyncio.gather(*tasks)
    except:
        for t in tasks:
            t.close()

if __name__ == '__main__':
    asyncio.run(main())
