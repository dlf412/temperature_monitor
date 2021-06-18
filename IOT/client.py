#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/11 20:31 
# @Author : Denglingfei 
# @File : client.py 

# 客户端
import socket
import time

import serial
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from IOT.utils import crc16

realdata = bytes([0x01, 0x03, 0x0E, 0, 0, 0, 0x9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xC1, 0x89])
event_summary = bytes([1, 3, 0x0A, 0, 0, 0, 0, 0x0A, 0x61, 0, 0, 0, 1, 0x58, 0x14])
event_write = bytes([1, 0x10, 0xE0, 0x10, 0, 0x02, 0x77, 0xCD])
event_data = bytes([1, 3, 0x10, 0, 0, 0x0A, 0x61, 0, 0, 0, 0x09, 0x0E, 0x10, 0x0E, 0x9C, 0, 0x05,
                   0x9E, 0x85, 0xFF, 0x9F])



class Client():
    def send_info(self):
        try:
            client = socket.socket()  # 定义协议类型,相当于生命socket类型,同时生成socket连接对象
            client.connect(('127.0.0.1', 7660))
            # x=serial.Serial('com3',9600,timeout=1)
            while True:
                msg = "uuid:123456"
                client.send(msg.encode("utf-8"))
                data = client.recv(1024)  # 这里是字节1k
                print(data)
                # recv = x.send(data)
                client.send(realdata)
                data = client.recv(1024)
                print(data)
                client.send(event_summary)
                data = client.recv(1024)
                print(data)
                client.send(event_write)
                data = client.recv(1024)
                print(data)

                client.send(event_data)
                data = client.recv(1024)

                print(data)

                time.sleep(20)

            client.close()
        except ConnectionError as ex:
            print(ex)


if __name__ == "__main__":
    client = Client()
    client.send_info()