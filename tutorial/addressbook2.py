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


class AddressBook(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)
        pass

    def addContact(self):
        pass

    def submitContact(self):
        pass

    def cancel(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addressBook = AddressBook()
    addressBook.show()
    sys.exit(app.exec())
