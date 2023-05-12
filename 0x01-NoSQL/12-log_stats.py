#!/usr/bin/env python3
"""
script that provides some stats about
Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginxStatsCount():
    """Returns stats about nginx logs"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    collections = nginx_collection.count_documents({})
    print(f'{collections} logs')
    print('Methods:')
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_count = nginx_collection.count_documents({"method": method})
