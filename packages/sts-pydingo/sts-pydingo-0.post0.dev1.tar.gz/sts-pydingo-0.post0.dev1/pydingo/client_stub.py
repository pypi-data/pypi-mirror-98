import asyncio
import itertools
import json
import threading
import urllib

import tornado
import tornado.websocket

class ClientStub(object):
    def __init__(self, loop = None):
        if (loop is None):
            loop = asyncio.new_event_loop()

        self.loop = loop
        self.ids = itertools.count()
        self.futs = {}

        th = threading.Thread(target = self.loop.run_forever)
        th.start()

    @property
    def hostname(self):
        parts = urllib.parse.urlsplit(self.ws.request.url)
        return parts.hostname

    @property
    def port(self):
        parts = urllib.parse.urlsplit(self.ws.request.url)
        return parts.port

    async def _connect(self, hostname, port):
        url = 'ws://' + hostname + ':' + str(port)
        self.ws = await tornado.websocket.websocket_connect(url)

    def connect(self, address, port):
        fut = asyncio.run_coroutine_threadsafe(self._connect(address, port), self.loop)
        fut.result()

        asyncio.run_coroutine_threadsafe(self.run(), self.loop)

    async def run(self):
        while True:
            msg = await self.ws.read_message()
            if (msg is None):
                return

            msg = json.loads(msg)
            buffer_count = msg.get('buffers', 0)

            msg = msg['detail']

            obj = msg['result']

            bufs = []
            for buffer in range(buffer_count):
                buf = await self.ws.read_message()
                bufs.append(buf)

            fut = self.futs.pop(msg['id'])
            fut.set_result((obj, bufs))

    def remote_call(self, method, *args, object_type = None, wait = True, return_buffers = False):
        id = next(self.ids)

        msg = {'id': id, 'method': method, 'params': args}
        msg = {'detail': msg}

        self.ws.write_message(json.dumps(msg))

        fut = self.loop.create_future()
        self.futs[id] = fut

        if wait:
            ev = threading.Event()
            fut.add_done_callback(lambda x: ev.set())

            ev.wait()

            obj, bufs = fut.result()
            if (object_type is not None):
                obj = object_type(obj)

            if return_buffers:
                return obj, bufs

            return obj
