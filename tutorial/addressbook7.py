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


class AddressBook(QtWidgets.QWidget):
    NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)
        pass

    def addContact(self):
        pass

    def editContact(self):
        pass

    def submitContact(self):
        pass

    def cancel(self):
        pass

    def removeContact(self):
        pass

    def next(self):
        pass

    def previous(self):
        pass

    def findContact(self):
        pass

    def updateInterface(self, mode):
        pass

    def saveToFile(self):
        pass

    def loadFromFile(self):
        pass

    def exportAsVCard(self):
        pass
