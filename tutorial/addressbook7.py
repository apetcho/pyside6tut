#!/usr/bin/env python3
import pickle
from PySide6 import QtCore
from PySide6 import QtWidgets


class SortedDict(dict):
    class Iterator:
        def __init__(self, sorted_dict: dict):
            pass

        def __iter__(self):
            return self

        def next(self):
            pass

        __next__ = next

    def __iter__(self):
        return SortedDict.Iterator(self)

    iterkeys = __iter__



