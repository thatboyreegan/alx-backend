#!/usr/bin/env python 3
"""This modlue has the index_range function"""

from typing import Tuple


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
