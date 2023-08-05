"""Utility functions"""
import logging
import inspect


def get_class_logger(obj):
    """
    Obtain a logger object for a class.
    :param obj: the class object
    :return: the logger
    """
    klass = list(filter(lambda m: m[0] == '__class__', inspect.getmembers(obj)))[0][1]
    cls_name = str(klass)[8:-2]
    return logging.getLogger(cls_name)
