#!/usr/bin/env python3
import pickle
from PySide6 import QtCore
from PySide6 import QtWidgets


class SortedDict(dict):
    class Iterator:
        def __init__(self, sorted_dict: dict):
            self._dict = sorted_dict
            self._keys = sorted(self._dict.keys())
            self._nr_items = len(self._keys)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._idx >= self._nr_items:
                raise StopIteration

            key = self._keys[self._idx]
            val = self._dict[key]
            self._idx += 1

            return (key, val)

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


class FindDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        pass

    def findClicked(self):
        pass

    def getFindText(self):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec())
