import asyncio
import threading
import uuid
import os

from fogverse import Consumer
from flask import Flask, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv

from fogverse.logging import CsvLogging

def page_not_found(*args):
  return render_template('404.html'), 404

app = Flask(__name__)
app.register_error_handler(404, page_not_found)
socketio = SocketIO(app)

class MyClient(CsvLogging, Consumer):
    def __init__(self, socket: SocketIO, loop=None):
        self.socket = socket
        self.auto_encode = False
        self.topic_pattern = os.getenv('TOPIC_PATTERN')
        self.consumer_conf = {'group_id': str(uuid.uuid4())}
        log_filename = f"logs/log_{self.__class__.__name__}_{os.getenv('SCENARIO', 'with_cloud')}.csv"
        CsvLogging.__init__(self, filename=log_filename)
        Consumer.__init__(self,loop=loop)

    async def receive(self):
        await asyncio.sleep(1)
        return b"halo"

    async def send(self, data):
        namespace = f'/final_uav_1'
        self.socket.emit('frame', data, namespace=namespace)

@app.route('/<uav_id>')
def index(uav_id=None):
    if not uav_id:
        return page_not_found()
    return render_template('index.html')

async def main(loop):
    consumer = MyClient(socketio, loop=loop)
    tasks = [consumer.run()]
    try:
        await asyncio.gather(*tasks)
    finally:
        for t in tasks:
            t.close()

def run_consumer(loop):
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()

if __name__ == '__main__':
    load_dotenv()
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=run_consumer, args=(loop,))
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False)
