#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 17:30
# @Author  : Sand
# @FileName: 客户端.py
# @Project : OldBoy
import socket
import struct
import json
import os


class MyTCPClient:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_packet_size = 8192
    coding = 'gbk'
    requst_queue_size = 5

    def __init__(self, server_address, connect=True):
        self.server_address = server_address
        self.socket = socket.socket(self.address_family, self.socket_type)

        if connect:
            try:
                self.client_connect()
            except Exception as e:
                self.client_close()
                raise

    def client_connect(self):
        self.socket.connect(self.server_address)

    def client_close(self):
        self.socket.close()

    def run(self):
        while True:
            inp = input('--->:').strip()
            if not inp: continue
            l = inp.split()
            cmd = l[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(l)

    def put(self, args):
        cmd = args[0]
        filename = args[1]
        if not os.path.isfile(filename):
            print('file:s% si not exists' % filename)
            return
        else:
            filesize = os.path.getsize(filename)

        head_dic = {'cmd': cmd, 'filename': os.path.basename(filename), 'filesize': filesize}
        print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding=self.coding)

        head_struct = struct.pack('i', len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.setsockopt(head_json_bytes)
        send_size = 0
        with open(filename, 'rb') as f:
            for line in f:
                self.socket.send(line)
                send_size += len(line)
                print(send_size)
            else:
                print('upload successful')


client = MyTCPClient(('127.0.0.1', 8080))
client.run()
