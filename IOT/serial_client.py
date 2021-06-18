#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/12 14:32 
# @Author : Denglingfei 
# @File : serial_client.py 

import serial

from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from sys import stdout

import time
from threading import Thread

from queue import Queue, Empty

class SerialAgent(Protocol):

    def __init__(self):
        self.serial = None
        # self.serial = serial.Serial('com3',9600,timeout=1)
        self._queue = Queue(maxsize=1)


    def heartbeat(self):
        while True:
            try:
                data = self._queue.get(block=True, timeout=30)
                self.transport.write(data)
            except Empty as err:
                print("发送心跳")
                self.transport.write(b"uuid:222222")
                time.sleep(30)
            except:
                import  traceback
                traceback.print_exc()


    def connectionMade(self):
        try:
            self.serial = serial.Serial('com3',9600,timeout=2)
        except Exception:
            print("打开串口失败")
        self.thr = Thread(target=self.heartbeat)
        self.thr.setDaemon(True)
        self.thr.start()
        self._queue.put(b"uuid:222222")

    def connectionLost(self, reason):
        if self.serial:
            self.serial.close()

    def dataReceived(self, data):
        print("recive:", data)
        if self.serial:
            print (self.serial.write(data))
            try:
                while True:
                    read_bytes = self.serial.read(40)
                    if read_bytes:
                        break
            except Exception as err:
                print (err)
            print("serial read:", read_bytes)
            self._queue.put(read_bytes)
            # self.transport.write(read_bytes)


class SerialClientFactory(ReconnectingClientFactory):

    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        p = SerialAgent()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)




if __name__ == '__main__':
    from twisted.internet import reactor
    reactor.connectTCP('127.0.0.1', 7660, SerialClientFactory())
    reactor.run()