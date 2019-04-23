from pymongo import MongoClient


class CET6CatDB:
    """连接MongoDB用"""
    conn = MongoClient('127.0.0.1', 27017)
    # collection:错误单词
    fault_words = conn.cet6cat.fault_words
