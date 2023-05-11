#!/usr/bin/env python3
"""Module implements an expiring web cache and tracker"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_client = redis.Redis()
"""Redis instance"""


def cache_data(method: Callable) -> Callable:
    """Caches the output of fetched data."""
    @wraps(method)
    def invoker(url) -> str:
        """The wrapper function to cache the output."""
        redis_client.incr(f'count:{url}')
        result = redis_client.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_client.set(f'count:{url}', 0)
        redis_client.setex(f'result:{url}', 10, result)
        return result
    return invoker


@cache_data
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the response to a request,
    and tracks the request.
    """
    return requests.get(url).text
