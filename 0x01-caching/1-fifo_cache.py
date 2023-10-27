#!/usr/bin/python3
"""THis module implements the class FIFOCache"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """This class inherits from BaseCaching and implements FIFO caching"""
    def __init__(self):
        """initializes an instance of the class"""
        super(FIFOCache, self).__init__()

    def put(self, key, item):
        """
        adds an item into the cache dict
        Args:
            key (str): key associated with the item
            item(str): value to be added to the dict
        """

        if key and item:
            self.cache_data[key] = item

        if BaseCaching.MAX_ITEMS < len(self.cache_data):
            first_key = next(iter(self.cache_data))
            self.cache_data.pop(first_key)
            print(f"DISCARD: {first_key}")

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
            return self.cache_data.get(key, None)
        return None
