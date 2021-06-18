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
                self.transport.write(b"uuid:999999")
            time.sleep(30)

    def connectionMade(self):
        self.serial = serial.Serial('com3',9600,timeout=1)
        self.thr = Thread(target=self.heartbeat)
        self.thr.setDaemon(True)
        self.thr.start()
        self._queue.put(b"uuid999999")

    def connectionLost(self, reason):
        self.serial.close()

    def dataReceived(self, data):
        if self.serial:
            self.serial.write(data)
            read_bytes = self.serial.read_all()
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