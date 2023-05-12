#!/usr/bin/env python3
"""
Module defines a function that returns the list
of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """returns a list of schools with a specific topic"""
    result = mongo_collection.find({'topics': topic})
    return list(result)
