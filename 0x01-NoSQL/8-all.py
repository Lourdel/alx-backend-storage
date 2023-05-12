#!/usr/bin/env python3
"""Module defines a function that lists all documents in a collection"""


def list_all(mongo_collection):
    """lists all documents in a a mongodb collections"""
    documents = []
    for document in mongo_collection.find():
        documents.append(document)
    return documents
