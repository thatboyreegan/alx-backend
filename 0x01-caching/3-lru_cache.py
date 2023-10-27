#!/usr/bin/python3
"""This module implements the class LRUCache"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """this class inherits from BaseCaching and implements LRU caching"""
    def __init__(self):
        """initializes a class instance"""
        super(LRUCache, self).__init__()
        self.Lru = []

    def put(self, key, item):
        """
        adds an item into the cache dict
        Args:
            key (str): key associated with the item
            item(str): value to be added to the dict
        """
        if key and item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                least_used = self.Lru.pop()
                del self.cache_data[least_used]
                print(f"DISCARD: {least_used}")

            if key in self.Lru:
                self.Lru.remove(key)
            self.Lru.insert(0, key)

    def get(self, key):
        """
        returns a value associated with the provided key

        Args:
            Key (str): key whose value is to be returned
        Returns:
            str: a value related to the key or None if key is none or
            not in the dict
        """
        if key:
            item = self.cache_data.get(key, None)
        if item:
            self.Lru.remove(key)
            self.Lru.insert(0, key)
        return item
