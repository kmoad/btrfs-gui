#!/usr/bin/env python3

import socket
import sys 
import time
import pickle
import struct
import traceback

class BtrfsDaemonClient(object):
    def __init__(self, client):
        self._socket = client

    def request(self, obj):
        data = pickle.dumps(obj)
        self._send(data)
        resp_raw = self._recv_msg()
        return pickle.loads(resp_raw)

    def _send(self, data):
        data = struct.pack('>I', len(data)) + data
        self._socket.sendall(data)

    def _recv_msg(self):
        raw_msglen = self._recv_data(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self._recv_data(msglen)

    def _recv_data(self, length):
        data = b''
        while len(data) < length:
            packet = self._socket.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.connect("/tmp/test")
    client = BtrfsDaemonClient(sock)

    while True:
        msg = input('> ')
        req = msg.strip().split()
        if req[0] in {'cat','ls'}:
            resp = client.request(req)
            if isinstance(resp, Exception):
                print(resp)
            elif req[0] == 'cat':
                print(resp)
            elif req[0] == 'ls':
                for ftype, fname in resp:
                    print(ftype, fname)