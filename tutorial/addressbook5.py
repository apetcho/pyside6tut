#!/usr/bin/env python3
from PySide6 import QtCore
from PySide6 import QtWidgets


class SortedDict(dict):
    class Iterator:
        def __ini__(self, sorted_dict):
            pass

        def __iter__(self):
            return self

        def next(self):
            pass

        __next__ = next

    def __iter__(self):
        pass

    iterkeys = __iter__



class AddressBook(QtWidgets.QWidget):
    NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
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


class FindDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
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
