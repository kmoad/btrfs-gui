#!/usr/bin/env python3

from socketserver import UnixStreamServer, StreamRequestHandler
import os
import struct
import pickle
from pathlib import Path
import traceback

socket_path = '/tmp/test'
if os.path.exists(socket_path):
    os.unlink(socket_path)

class Handler(StreamRequestHandler):
    def handle(self):
        while True:
            raw_msglen = self._recv_data(4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('>I', raw_msglen)[0]
            raw_msg = self._recv_data(msglen)
            msg = pickle.loads(raw_msg)
            if msg[0] == 'cat':
                resp = self._cat(msg)
            elif msg[0] == 'ls':
                resp = self._ls(msg)
            else:
                self._send(pickle.dumps(ValueError(msg[0])))

    def _cat(self, msg):
        try:
            path = Path(msg[1])
            if not path.is_file():
                self._send('')
            with open(msg[1]) as f:
                ret = f.read()
        except Exception as e:
            traceback.print_exc()
            ret = e
        self._send(pickle.dumps(ret))

    def _ls(self, msg):
        try:
            directory = Path(msg[1])
            ret = []
            for item in directory.iterdir():
                if item.is_dir():
                    ret.append(('d', str(item)))
                elif item.is_file():
                    ret.append(('f', str(item)))
        except Exception as e:
            traceback.print_exc()
            ret = e
        self._send(pickle.dumps(ret))

    def _send(self, data):
        data = struct.pack('>I', len(data)) + data
        self.request.sendall(data)

    def _recv_data(self, length):
        data = b''
        while len(data) < length:
            packet = self.request.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data

with UnixStreamServer('/tmp/test', Handler) as server:
    os.chown(socket_path, 1000, 1000)
    os.chmod(socket_path, 0o600)
    server.serve_forever()
