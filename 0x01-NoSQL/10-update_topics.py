#!/usr/bin/env python3
"""
Module defines a function that changes all topics
of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """updates all topics in a document by name"""
    result = mongo_collection.update_many({'name': name},
                                          {'$set': {'topics': topics}})
