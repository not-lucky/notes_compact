"""
03-lfu-cache.py

Implementation of Least Frequently Used (LFU) Cache.
"""

from collections import defaultdict

class DLinkedNode:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_first(self, node: DLinkedNode):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: DLinkedNode):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_last(self) -> DLinkedNode:
        if self.size == 0:
            return None
        last = self.tail.prev
        self.remove(last)
        return last

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.cache = {}
        self.freq_map = defaultdict(DoublyLinkedList)

    def _update_freq(self, node: DLinkedNode):
        freq = node.freq
        self.freq_map[freq].remove(node)
        if self.freq_map[freq].size == 0 and self.min_freq == freq:
            self.min_freq += 1

        node.freq += 1
        self.freq_map[node.freq].add_first(node)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._update_freq(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._update_freq(node)
        else:
            if len(self.cache) >= self.capacity:
                lfu_list = self.freq_map[self.min_freq]
                removed = lfu_list.remove_last()
                del self.cache[removed.key]

            new_node = DLinkedNode(key, value)
            self.cache[key] = new_node
            self.freq_map[1].add_first(new_node)
            self.min_freq = 1
