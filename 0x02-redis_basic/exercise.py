#!/usr/bin/env python3
"""Module implements the class Cache"""

import redis
from typing import Union
import uuid


class Cache:
    """connects to redis"""
    def __init__(self):
        self._redis = redis.Redis(host="localhost", port=6379)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data and returns a key as a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
