#!/usr/bin/env python3
"""Module implements the class Cache"""

import redis
from typing import Union, Optional, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Returns the number of times methods of Cache are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapped function to use method's name as the key
        for counting its call
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator stores the history of inputs and
    outputs for a particular function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for decorator functionality """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(method: Callable):
    """
    Displays the history of calls of a particular
    function
    """
    method_key = method.__qualname__
    r = redis.Redis()
    input_data = method_key + ":inputs"
    output_data = method_key + ":outputs"
    method_count = r.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    input_list = r.lrange(input_data, 0, -1)
    output_list = r.lrange(output_data, 0, -1)
    for key, val in list(zip(input_list, output_list)):
        attr, val = key.decode('utf-8'), val.decode('utf-8')
        print(f'{method_key}(*{attr}) -> {val}')


class Cache:
    """connects to redis"""
    def __init__(self):
        """ Initialize a new Cache object with a Redis instance"""
        self._redis = redis.Redis(host="localhost", port=6379)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data and returns a randomly generated key as a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Gets value & returns the desired data type"""
        data_value = self._redis.get(key)
        if fn is not None:
            return fn(data_value)
        return data_value

    def get_str(self, data_value: str) -> str:
        """returns string equivalent from data"""
        return data_value.decode('utf-8')

    def get_int(self, data_value: str) -> int:
        """returns int equivalent from data"""
        return int(data_value)
