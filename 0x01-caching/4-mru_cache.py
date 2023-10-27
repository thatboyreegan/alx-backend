#!/usr/bin/python3
"""This module implements the class MRUCache"""

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """This claas inherits from BaseCaching and implements MRU caching"""
    def __init__(self):
        """initializes a class instance"""
        super(MRUCache, self).__init__()
        self.mru = []

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
                last_item = self.mru.pop()
                del self.cache_data[last_item]
                print(f"DISCARD: {last_item}")

            if key in self.mru:
                self.mru.remove(key)
            self.mru.append(key)

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
            self.mru.remove(key)
            self.mru.append(key)
        return item
