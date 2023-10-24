#!/usr/bin/env python3
"""this module has index_range and a class"""

import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """"
    return a tuple of size two containing a start index and an
    end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters

    Args:
        page (int): the page number
        page_size (int): size of the page
    Returns:
        Tuple [int, int]: a tuple of the start and end indexes
    """
    start = page_size * (page - 1)
    end = page_size * page

    return start, end


class Server:
    """Server class to paginate a database of popular baby names.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes new Server"""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """gets items in the desired page.

        Args:
            page (int, optional): Page number, defaults to 1.
            page_size (int, optional): Number of items in a page.
                Defaults to 10.

        Returns:
            List[List]: List of items in the page or an empty list if page
                is not found.
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        start, end = index_range(page, page_size)

        try:
            items = self.dataset()[start:end]
        except IndexError:
            items = []

        return items

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Returns a dictionary containing the following key-value pairs:

        - `page_size`: the length of the returned dataset page
        - `page`: the current page number
        - `data`: the dataset page (equivalent to return from `get_page`)
        - `next_page`: number of the next page, None if no next page
        - `prev_page`: number of the previous page, None if no previous page
        - `total_pages`: the total number of pages in the dataset as an integer

        Args:
            page (int, optional): Page number. Defaults to 1.
            page_size (int, optional): Number of items per page.
                Defaults to 10.

        Returns:
            Dict: Dictionary with the format above.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = (page + 1 <= total_pages and page + 1) or None
        prev_page = (page - 1 > 0 and page - 1) or None

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages,
        }
