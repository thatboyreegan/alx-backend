#!/usr/bin/env python3
"""
this module has class Server"""


import csv
import math
from typing import List, Dict, Optional


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize new Server"""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(
        self, index: Optional[int] = None, page_size: int = 10
    ) -> Dict:
        """A get method that retains the ordering of the data even when
        some modifications such as deletion are made on the existing data.

        Returns a dictionary with th format:
        - `index`: the current start index of the return page.
        - `next_index`: the next index to query with.
        - `page_size`: the current page size
        - `data`: the actual page of the dataset

        Args:
            `index` (Optional[int], optional): Index of the item to start
                paging. Defaults to None.
            `page_size` (int, optional):Number of items per page.
                Defaults to 10.

        Returns:
            Dict: Dictionary with the format shown above.
        """
        indexed_dataset = self.indexed_dataset()

        assert index and (
            index in indexed_dataset.keys() or index < len(indexed_dataset)
        )

        data = []

        item_index = index
        for i in range(page_size):
            item = indexed_dataset.get(item_index)

            while not item and item_index < len(indexed_dataset):
                item_index += 1
                item = indexed_dataset.get(item_index)

            if item:
                data.append(item)

            if item_index >= len(indexed_dataset):
                break

            item_index += 1

        next_index = None
        for i in range(index + page_size, len(indexed_dataset)):
            if indexed_dataset.get(i):
                next_index = i
                break

        if next_index and next_index < item_index:
            next_index = item_index

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index,
        }
