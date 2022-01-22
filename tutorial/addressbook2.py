#!/usr/bin/env python3
from PySide6 import QtCore
from PySide6 import QtWidgets


class SortedDict(dict):
    class Iterator:
        def __init__(self, soreted_dict):
            pass

        def __iter__(self):
            pass

        def next(self):
            pass

        __next__ = next

    def __iter__(self):
        pass

    iterkeys = __iter__


