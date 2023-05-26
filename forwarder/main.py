import asyncio
import uuid
import os

from fogverse import Consumer, Producer
from fogverse.logging import CsvLogging

class LocalForwarder(CsvLogging, Consumer, Producer):
    def __init__(self):
        self.auto_decode = False
        self.auto_encode = False
        log_filename = f"logs/log_{self.__class__.__name__} \
                        _{os.getenv('ROLE')} \
                        _{os.getenv('UAV_COUNT')}_uav \
                        _attempt_{os.getenv('ATTEMPT')}.csv"
        CsvLogging.__init__(self, filename=log_filename)
        Consumer.__init__(self)
        Producer.__init__(self)

# ======================================================================
class LocalForwarder2(LocalForwarder):
    def __init__(self):
        self.consumer_conf = {'group_id': str(uuid.uuid4())}
        super().__init__()

ROLES = {
    "local2cloud": LocalForwarder,
    "cloud2local": LocalForwarder2,
}

async def main():
    role = os.getenv('ROLE')
    _Forwarder = ROLES[role]
    Forwarder = _Forwarder()
    tasks = [Forwarder.run()]
    try:
        await asyncio.gather(*tasks)
    except:
        for t in tasks:
            t.close()

if __name__ == '__main__':
    asyncio.run(main())
