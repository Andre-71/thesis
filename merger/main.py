import asyncio
import bisect
import os
import uuid

from fogverse import ConsumerStorage, Producer, Consumer
from fogverse.util import (
    calc_datetime, compress_encoding, get_timestamp, get_timestamp_str,
    numpy_to_base64_url, recover_encoding, timestamp_to_datetime
)
from util import box_label

ENCODING = os.getenv('ENCODING', 'jpg')

class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

class MyConsumerStorage(Consumer, ConsumerStorage):
    def __init__(self):
        self.consumer_topic = ['input', 'result']
        self.consumer_conf = {'group_id': str(uuid.uuid4())}
        self.auto_encode = False
        self._data = {}
        Consumer.__init__(self)
        ConsumerStorage.__init__(self)

    def get_data(self):
        return self._data

    def _after_receive(self, data):
        super()._after_receive(data)
        headers = {key: value for key, value in data.headers}
        data.headers = headers
        uav_id = headers['uav'].decode()
        self._data.setdefault(uav_id, {
            'last_frame_idx': -1,
            'timestamp': get_timestamp_str(),
            'data': [],
            'max_delay': -1,
            'max_delay_frame': -1,
        })

        if data.topic == 'input': return data
        return data

    def decode(self, data):
        headers = self.message.headers
        if headers is not None:
            self.message.headers = {**headers,
                'frame': int(headers['frame']),
                'timestamp': timestamp_to_datetime(headers['timestamp']),
                'uav': headers['uav'].decode(),
                'type': headers.get('type', b'').decode()}
        return super().decode(data)

    def process(self, data):
        if self.message.topic == 'input':
            data = compress_encoding(data, ENCODING)
        self.message.value = ''
        return data

    def on_input_send(self, data, uav_id, frame_idx):
        last_frame_idx = self._data[uav_id]['last_frame_idx']
        if last_frame_idx != -1 and frame_idx <= last_frame_idx:
            return
        lst_data = self._data[uav_id]['data']
        idx = bisect.bisect_left(KeyWrapper(lst_data,
                                lambda x: x['message'].headers['frame']),
                                frame_idx)
        obj = {
            'message': self.message,
            'data': data,
            'input_timestamp': get_timestamp(),
            'final_timestamp': -1,
            'delay': 0,
            'type': 'input',
            'from': 'input'
        }
        lst_data.insert(idx, obj)

    def on_inference_send(self, pred, uav_id, frame_idx):
        uav_data = self._data[uav_id]
        lst_data = uav_data['data']
        for _data in lst_data:
            if _data['message'].headers['frame'] != frame_idx: continue
            frame = recover_encoding(_data['data'])
            box_label(pred, frame, relative=True, inplace=True)
            _delay = calc_datetime(_data['input_timestamp'])
            _data['delay'] = _delay
            _data['final_timestamp'] = get_timestamp()
            if _delay > uav_data['max_delay']:
                uav_data['max_delay'] = max(uav_data['max_delay'],_delay)
                uav_data['max_delay_frame'] = frame_idx
            _data['data'] = numpy_to_base64_url(frame, ENCODING)
            _data['message'].headers = self.message.headers
            _data['type'] = 'final'
            _data['from'] = 'cloud'

    def on_final_send(self, data, uav_id ,frame_idx):
        uav_data = self._data[uav_id]
        lst_data = uav_data['data']
        for _data in lst_data:
            if _data['message'].headers['frame'] != frame_idx: continue
            _delay = calc_datetime(_data['input_timestamp'])
            _data['delay'] = _delay
            _data['final_timestamp'] = get_timestamp()
            if _delay > uav_data['max_delay']:
                uav_data['max_delay'] = max(uav_data['max_delay'],_delay)
                uav_data['max_delay_frame'] = frame_idx
            _data['data'] = data
            _data['message'].headers = self.message.headers
            _data['type'] = 'final'
            _data['from'] = 'local-inferencer'

    async def send(self, data):
        headers = self.message.headers
        data_type = headers.get('type')
        uav_id = headers['uav']
        frame_idx = headers['frame']
        if self.message.topic == 'input':
            self.on_input_send(data, uav_id, frame_idx)
        elif data_type == 'inference':
            self.on_inference_send(data, uav_id, frame_idx)
        elif data_type == 'final':
            self.on_final_send(data, uav_id, frame_idx)

def print_message(message):
    indent = ' '*2
    for uav_id, uav_data in message.items():
        print(f'{uav_id}:')
        for attr_uav, value_uav in uav_data.items():
            if attr_uav == 'data':
                for msg in value_uav:
                    _type = msg.get('type')
                    _frame = msg['message'].headers['frame']
                    _input_timestamp = msg.get('input_timestamp')
                    _final_timestamp = msg.get('final_timestamp')
                    print(f'{indent*2}- type: {_type}')
                    print(f'{indent*2}  frame: {_frame}')
                    print(f'{indent*2}  input timestamp: {_input_timestamp}')
                    print(f'{indent*2}  final timestamp: {_final_timestamp}')
            else:
                print(f'{indent}{attr_uav}: {value_uav}')

def print_send_data(send_data):
    indent = ' '*2
    for uav_id, uav_data in send_data.items():
        print(f'{uav_id}:')
        for attr_uav, value_uav in uav_data.items():
            if attr_uav == 'data':
                print(f'{indent}data:')
                for msg in value_uav:
                    headers = msg['headers']
                    _frame = headers['frame']
                    _from = msg['from']
                    print(f'{indent*2}  frame: {_frame} {_from}')
            else:
                print(f'{indent}{attr_uav}: {value_uav}')

class MyProducer(Producer):
    def __init__(self, consumer_storage, loop=None):
        self.consumer = consumer_storage
        self.auto_decode = False
        self.auto_encode = False
        self.avg_delay = 0
        self.n_avg_delay = 0
        self.thresh = int(os.getenv('WAIT_THRESH', 2000))
        self._loop = loop or asyncio.get_event_loop()
        Producer.__init__(self)

    @property
    def data(self):
        return self.consumer.get_data()

    async def receive(self):
        data = self.data
        await asyncio.sleep(self.thresh / 1e3)
        return data
    
    async def send(self, data):
        return data

    def process(self, *args):
        send_data = {}
        for uav_id, uav_data in self.message.items():
            if len(uav_data['data']) == 0: continue
            elapsed = calc_datetime(uav_data['timestamp'])
            if elapsed < self.thresh: continue
            frames = uav_data['data']
            send_frames = [{
                    'data': i['data'],
                    'headers': i['message'].headers,
                    'from': i['from']}
                for i in frames if i['type'] == 'final']
            if len(send_frames) == 0: continue
            avg_delay = self.thresh / len(send_frames)
            self.avg_delay = (self.avg_delay * self.n_avg_delay + avg_delay) \
                / (self.n_avg_delay + 1)
            self.n_avg_delay += 1
            send_data[uav_id] = {
                'avg_delay': avg_delay,
                'data': send_frames,
            }
            if frames:
                uav_data['last_frame_idx'] = \
                    frames[-1]['message'].headers['frame']
            uav_data['data'] = []
            uav_data['timestamp'] = get_timestamp()
        return send_data

    def _send(self, uav_id, data, headers):
        topic = f'final_{uav_id}'
        task = super().send(data.encode(), topic=topic, headers=headers)
        self._loop.create_task(task)

    async def send(self, data):
        if not data: return
        print_send_data(data)
        for uav_id, uav_data in data.items():
            delay = uav_data['avg_delay']
            for i in range(len(uav_data['data'])):
                frame = uav_data['data'][i]
                headers = frame['headers']
                headers = [
                    ('uav', headers.get('uav', '').encode()),
                    ('frame', str(headers.get('frame')).encode()),
                    ('timestamp', get_timestamp_str(
                        headers.get('timestamp')).encode()),
                    ('type', str(headers.get('type')).encode()),
                    ('from', str(frame['from']).encode()),
                ]
                _data = frame['data']
                _delay = delay * (i+1) / 1e3
                self._loop.call_later(_delay, self._send, uav_id,
                                      _data, headers)

async def main():
    consumer = MyConsumerStorage()
    producer = MyProducer(consumer)
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
