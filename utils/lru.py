#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/16 16:23 
# @Author : Denglingfei 
# @File : lru.py

class Node(object):
    def __init__(self, key, data, next=None, pre=None):
        self.key = key
        self.data = data
        self.next = next
        self.pre = pre

    def __str__(self):
        return f"Node({self.key}:{self.data})"

    def __repr__(self):
        return f"Node({self.key}:{self.data})"


class LRUCache(object):
    def __init__(self, cap):
        self.size = 0
        self.cap = cap
        self.map = {}
        self.head = None
        self.tail = None


    def __str__(self):

        cur = self.head
        ret = ""
        while cur:
            ret += str(cur)
            cur = cur.next
        return ret

    def remove(self, key):
        if key not in self.map:
            return
        if self.size == 1:
            node = self.map[key]
            self.head = self.tail = None
        else:
            node = self.map[key]
            if node == self.tail:
                self.tail = self.tail.pre
                self.tail.next = None
            elif node == self.head:
                self.head = self.head.next
                self.head.pre = None
            else:
                node.pre.next, node.next.pre = node.next, node.pre
        del node
        self.size -= 1

    def put(self, key, value):

        node = self.get(key)
        if node:
            node.data = value
            return

        if self.size >= self.cap:
            rm_key = self.head.key
            self.head = self.head.next
            self.head.pre = None
            del self.map[rm_key]
            self.size -= 1

        node = Node(key, value)
        self.map[key] = node
        if self.size == 0:
            self.head = self.tail = node
            self.size = 1
            return
        else:
            self.tail.next = node
            node.pre = self.tail
            self.tail = node
            self.size += 1

    def get(self, key):
        node = self.map.get(key, None)
        if node:
            # 是最后一个节点，直接返回
            if self.tail == node:
                return node
            else:  # 否则将移动到最后一个节点处
                # 如果有前继节点
                if node.pre:
                    node.pre.next, node.next.pre = node.next, node.pre
                else:
                    node.next.pre = None
                    self.head = node.next
                self.tail.next = node
                node.pre = self.tail
                self.tail = node
                node.next = None

            return node

        return None


def test():
    cache = LRUCache(5)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    print(cache.get(1))
    cache.put(4, 4)
    cache.put(5, 5)

    print(cache)
    cache.put(6, 6)
    print(cache)
    cache.put(2, 8)
    print(cache)
    cache.put(7, 7)
    print(cache)

    cache.remove(5)
    print(cache)
    cache.put(6, 6)
    print(cache)
