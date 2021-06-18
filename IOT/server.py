#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/3/9 12:15
# @Author : Denglingfei
# @File : server.py

from datetime import datetime
import asyncio
import os
import sys
import threading
import time
import struct
import traceback

import ipaddress
from typing import DefaultDict

from twisted.internet import reactor
from twisted.internet.error import ConnectionLost
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

from twisted.logger import STDLibLogObserver, Logger

# import logging
# log = logging.getLogger("apilog")
# log = Logger(observer=STDLibLogObserver(name="iot"))
# log.startLogging(DailyLogFile.fromFullPath("iot_server.log"))
# log.startLogging(sys.stdout)

import django
from django.db.transaction import atomic
from django.db.models import Q, F

# 注册django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "temperature_monitor.settings")
django.setup()

from IOT.utils import crc16, obj_details
from pyrometer.models import *

log = Logger(observer=STDLibLogObserver(name="iot"))


WHITE_LIST = []
BLACK_LIST = []

MAX_CLIENTS_SAMEIP = 1


class ModbusProtocol(LineReceiver):

    def __init__(self, devices, clients):
        self.devices = devices
        self.clients = clients
        self.setRawMode()  # 二进制模式
        self.state = "idle"
        self.online_at = 0  # 上线的时间点
        self.uuid = ""
        self.cur_event_no = 0
        self.newest_event_no = 0
        self.ts = time.time()
        self.dev = None

    def idle(self, data):
        log.debug('I am idle...')
        return "I am idle"

    def heartbeat(self, data):

        if len(data) == 4:
            uuid = "test"
        else:
            uuid = data[5:].decode('utf-8')
        connected = self.devices.get(uuid)
        if connected and connected != self:
            self.transport.loseConnection()
            # self.connectionLost()
        elif connected is None:
            self.online_at = time.time()
            self.uuid = uuid
            self.dev, _ = Device.objects.update_or_create(
                uuid=self.uuid, defaults={
                    'is_online': True, 'last_online_time': datetime.now()})
            es = EventSummary.objects.filter(
                device=self.dev).only('sync_no').first()
            if es:
                self.cur_event_no = es.sync_no + 1
            else:
                self.cur_event_no = 1

            log.info(
                "device:%s online at %s, sync_no:%d" %
                (self.uuid, self.dev.last_online_time, self.cur_event_no - 1))
            self.devices[uuid] = self  # 将自己加入到devices中
        else:
            self.dev.last_online_time = datetime.now()
            self.dev.total_online_time = int(
                self.dev.total_online_time) + int(time.time() - self.online_at)
            self.dev.save(
                update_fields=(
                    'last_online_time',
                    'total_online_time'))
            self.online_at = time.time()

        # 发送读取实时数据的指令
        self.state = 'heartbeat'
        to_send = struct.pack(">BBHH", 0x01, 0x03, 0x1000, 0x0007)
        self.sendRaw(to_send + struct.pack(">H", crc16(to_send)))
        self.state = 'real_data'

    def real_data(self, data):
        fmt = ">HHHII"
        temperature, visitors, people_temperature, device_rtc_time, device_control_time = struct.unpack(
            fmt, data[3:-2])
        log.info(
            "收到实时数据:%s" %
            ((temperature,
              visitors,
              people_temperature,
              device_rtc_time,
              device_control_time),
             ))
        RealData.objects.get_or_create(
            device=self.dev,
            temperature=temperature,
            visitors=visitors,
            people_temperature=people_temperature,
            device_rtc_time=device_rtc_time,
            device_control_time=device_control_time)
        # 读取实时汇总消息
        to_send = struct.pack(">BBHH", 0x01, 0x03, 0xE000, 0x0005)
        self.sendRaw(to_send + struct.pack(">H", crc16(to_send)))
        self.state = 'event_summary'

    def event_summary(self, data):
        fmt = ">HII"
        max_record, self.newest_event_no, oldest_no = struct.unpack(
            fmt, data[3:-2])

        log.info(
            "收到报警汇总数据:%s" %
            ((max_record, self.newest_event_no, oldest_no),))
        # TODO: 将3个数据写到数据库中, 判断当前最后事件
        es, created = EventSummary.objects.update_or_create(
            device=self.dev,
            defaults={
                'newest_no': self.newest_event_no,
                'oldest_no': oldest_no,
                'max_record': max_record,
                })
        if created:
            es.sync_no = self.newest_event_no - 1  # 同步最后一条数据
            es.save(update_fields=('sync_no',))
            self.cur_event_no = self.newest_event_no

        if self.cur_event_no > self.newest_event_no:
            self.state = 'idle'
        else:  # // 写event是为了读
            self.cur_event_no = max(self.cur_event_no, oldest_no)
            to_send = struct.pack(
                ">BBHHBI",
                0x01,
                0x10,
                0xE010,
                0x0002,
                0x04,
                self.cur_event_no)
            self.sendRaw(to_send + struct.pack(">H", crc16(to_send)))
            self.state = 'event_write'

    def event_write(self, data):

        # 写响应成功(需要读取哪个事件编号需要先写)

        log.info("收到写报警数据响应")
        to_send = struct.pack(">BBHH", 0x01, 0x03, 0xE010, 0x0008)
        self.sendRaw(to_send + struct.pack(">H", crc16(to_send)))
        self.state = 'event_read'

    def event_read(self, data):

        fmt = ">IHHHHI"
        no, type, visitors, temperature, warn_temperature, warn_time = struct.unpack(
            fmt, data[3:-2])
        log.debug(
            "收到读报警响应:%s" %
            ((no, type, visitors, temperature, warn_temperature, warn_time),))

        if no == self.cur_event_no:  # 读到的和写的数据一致
            Event.objects.update_or_create(
                no=no, device=self.dev,
                defaults={"visitors":visitors,
                          "type": type,
                "temperature":temperature,
                "warn_temperature":warn_temperature,
                "warn_time":warn_time})
            self.cur_event_no += 1
            EventSummary.objects.filter(device=self.dev).update(sync_no=no)

        if self.cur_event_no > self.newest_event_no:
            self.state = 'idle'
        else:
            to_send = struct.pack(
                ">BBHHBI",
                0x01,
                0x10,
                0xE010,
                0x0002,
                0x04,
                self.cur_event_no)
            self.sendRaw(to_send + struct.pack(">H", crc16(to_send)))
            self.state = 'event_write'

    def connectionMade(self):
        client_ip = self.transport.client[0]
        if client_ip in BLACK_LIST:
            self.transport.loseConnection()
            return

        if not ipaddress.ip_address(
                client_ip).is_private and ipaddress not in WHITE_LIST:
            if len(self.clients[client_ip]) >= MAX_CLIENTS_SAMEIP:
                self.transport.loseConnection()
                return

        self.ts = time.time()
        log.info("client:%s connected" % str(self.transport.client))
        self.uuid = self.transport.client

        self.clients[client_ip].append(self)
        # obj_details(self.transport)
        # self.factory.numProtocols = self.factory.numProtocols + 1

    def connectionLost(self, reason):
        log.debug(str(reason))
        # 记录在线的时间, 将设备设置为下线
        if self.dev:

            online_ts = int(time.time() - self.online_at)
            # log.debug("online time is: %d" % self.online_time)
            Device.objects.filter(
                id=self.dev.id).update(
                is_online=False,
                total_online_time=F('total_online_time') +
                online_ts)

        if self.uuid in self.devices:
            del self.devices[self.uuid]
        if self.transport.client[0] in self.clients and \
                self in self.clients[self.transport.client[0]]:
            self.clients[self.transport.client[0]].remove(self)

    # def process(self, data):
    #     try:
    #         while self.state == "idle":
    #             time.sleep(0.1)
    #         print(type(self.state))
    #         func = getattr(self, self.state)
    #         assert callable(func)
    #         return func(data)
    #
    #     finally:
    #         self.state = "idle"

    def rawDataReceived(self, data):
        # 处理data
        try:
            self.ts = time.time()
            log.debug(str(data))
            if len(data) < 4:
                self.transport.loseConnection()
            if data[:5] == b'uuid:' or len(data) == 4:   # 设备的自动上报uuid，也就是心跳
                self.state = 'heartbeat'
                self.heartbeat(data)
            elif data[:4] == b'cmd:':  # 命令控制, 由上位机发起，格式为: "cmd:一位指令+设备uuid"
                self.sendCommand(data[4], data[5:])
            elif data[0] == 0x01 and data[1] == 0x03:  # 读响应
                assert len(data) == data[2] + 5
                if struct.unpack(">H", data[-2:])[0] != crc16(data[:-2]):
                    # print(struct.unpack(">H", data[-2:]), crc16(data[:-2]))
                    log.error("crc check error")
                    self.transport.loseConnection()
                else:
                    if self.dev:
                        if data[2] == 0x10:
                            self.state = "event_read"
                        elif data[2] == 0x0A:
                            self.state = 'event_summary'
                        elif data[2] == 0x0E:
                            self.state = 'real_data'
                        getattr(self, self.state)(data)
                    else:
                        log.error("设备未上线")

                # if self.state in ('realdata', 'event_summary', 'event_read', 'configure_read'):
                #     getattr(self, self.state)(data)
                # if self.state == 'realdata':
                #     self.realdata(data)
                # elif self.state == "event_summary":
                #     self.event_summary(data)
                # elif self.state == 'event_read':
                #     self.event_read(data)
                # elif self.state == 'configure_read':
                #     self.configure_read(data)
                # else:
                #     log.info("状态不对，自我修复")
                #     if self.uuid:
                #         if data[2] == 0x10:
                #             self.state = "event_read"
                #         elif data[2] == 0x0A:
                #             self.state = 'event_summary'
                #         elif data[2] == 0x0E:
                #             self.state = 'real_data'
                #         getattr(self, self.state)(data)
                #     else:
                #         log.error("设备未发送过心跳包")

            elif data[0] == 0x01 and data[1] == 0x10:  # 写响应
                assert len(data) == 8
                if struct.unpack(">H", data[-2:])[0] != crc16(data[:-2]):
                    log.error("crc check error")
                    self.transport.loseConnection()
                if self.state == 'event_write':
                    self.event_write(data)
                elif self.state == 'configure_write':
                    self.configure_write(data)
                else:
                    log.error("错误的状态")
            elif data[0] == 0x01 and data[1] in ('0x83', '0x90'):
                log.error("设备[%s]响应出错, 错误码[%d]" % (self.uuid, data[2]))
        except BaseException:
            log.error(traceback.format_exc())

    def sendRaw(self, raw):
        self.transport.write(raw)


class ModbusProtocolFactory(Factory):
    def __init__(self):
        self.devices = {}  # 在线设备
        self.clients = DefaultDict(list)  # 在线客户端
        self.running = True

    def pool_run(self):
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_forever()

    def buildProtocol(self, addr):
        return ModbusProtocol(self.devices, self.clients)

    async def check_client_online(self):
        while self.running:
            for key in list(self.clients.keys()):
                clients = self.clients[key]
                for client in clients:
                    if time.time() - client.ts > 90:
                        log.info("client:%s gone away" % key)
                        client.transport.loseConnection(ConnectionLost)
                    # device.connectionLost(reason=ConnectionLost)
            log.info("check client online or offline threading running....")
            await asyncio.sleep(30)

    async def task(self):
        await asyncio.create_task(self.check_client_online())

    def startFactory(self):
        log.debug("start Factory")
        # 在当前线程下创建时间循环，（未启用），在start_loop里面启动它
        self.event_loop = asyncio.new_event_loop()
        t = threading.Thread(target=self.pool_run)  # 通过当前线程开启新的线程去启动事件循环
        t.setDaemon(True)
        t.start()
        asyncio.run_coroutine_threadsafe(self.task(), self.event_loop)
        log.debug("end start Factory")

    def stopFactory(self):
        self.running = False


if __name__ == '__main__':
    listened = reactor.listenTCP(7660, ModbusProtocolFactory())
    log.info("[%s]server start ..." % listened)
    reactor.run()
