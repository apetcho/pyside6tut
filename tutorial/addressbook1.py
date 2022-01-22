#!/usr/bin/env python3
from ast import Add
from PySide6 import QtCore
from PySide6 import QtWidgets


class AddressBook(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addressbook = AddressBook()
    addressbook.show()
    sys.exit(app.exec())
