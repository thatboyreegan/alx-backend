#!/usr/bin/python3
"""This module implements the class BasicCache"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """This class inherits from Basecaching and implements basic caching"""
    def __init__(self):
        """
        intitializes a class instance
        """
        super(BasicCache, self).__init__()

    def put(self, key, item):
        """
        adds an item into the dictionary for caching
        Args:
            key (str): key associated with the value
            Item (str): value associated with key to be added to the dict
        """
        if key and item:
            self.cache_data[key] = item

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
