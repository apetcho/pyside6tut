#!/usr/bin/env python3
from PySide6 import QtCore
from PySide6 import QtWidgets


class SortedDict(dict):
    class Iterator:
        def __init__(self, soreted_dict):
            self._dict = soreted_dict
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

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)
        self.contacts = SortedDict()
        self.oldname = ""
        self.oldAddress = ""

        nameLabel = QtWidgets.QLabel("Name:")
        self.nameLine = QtWidgets.QLineEdit()
        self.nameLine.setReadOnly(True)

        addressLabel = QtWidgets.QLabel("Address:")
        self.addressText = QtWidgets.QTextEdit()
        self.addressText.setReadOnly(True)

        self.addButton = QtWidgets.QPushButton("&Add")
        self.submitButton = QtWidgets.QPushButton("&Submit")
        self.submitButton.hide()
        self.cancelButton = QtWidgets.QPushButton("&Cancel")
        self.cancelButton.hide()

        buttonLayout1 = QtWidgets.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton, QtCore.Qt.AlignTop)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addStretch()

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
