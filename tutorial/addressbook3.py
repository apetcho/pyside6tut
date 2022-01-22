#!/usr/bin/env python3
import numbers
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
        self.oldName = ""
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
        self.nextButton = QtWidgets.QPushButton("&Next")
        self.nextButton.hide()
        self.previousButton = QtWidgets.QPushButton("&Previous")
        self.previousButton.setEnabled(False)

        self.addButton.clicked.connect(self.addContact)
        self.submitButton.clicked.connect(self.submitContact)
        self.cancelButton.clicked.connect(self.cancel)
        self.nextButton.clicked.connect(self.next)
        self.previousButton.clicked.connect(self.previous)

        buttonLayout1 = QtWidgets.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton, QtCore.Qt.AlignTop)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addStretch()

        buttonLayout2 = QtWidgets.QHBoxLayout()
        buttonLayout2.addWidget(self.previousButton)
        buttonLayout2.addWidget(self.nextButton)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.addressText, 1, 1)
        mainLayout.addLayout(buttonLayout1, 1, 2)
        mainLayout.addLayout(buttonLayout2, 3, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.nameLine.setReadOnly(False)
        self.nameLine.setFocus(QtCore.Qt.OtherFocusReason)
        self.addressText.setReadOnly(False)

        self.addButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.previousButton.setEnabled(False)
        self.submitButton.show()
        self.cancelButton.show()

    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QtWidgets.QMessageBox.information(
                self, "Empty Field", "Please enter a name and address.")
            return

        if name not in self.contacts:
            self.contacts[name] = address
            QtWidgets.QMessageBox.information(
                self, "Add Successful",
                f'"{name}" has been added to your address book.'
            )
        else:
            QtWidgets.QMessageBox.information(
                self, "Add Unsuccessful",
                f'Sorry, "{name}" is already in your address book.' 
            )
            return

        if not self.contacts:
            self.nameLine.clear()
            self.addressText.clear()

        self.nameLine.setReadOnly(True)
        self.addressText.setReadOnly(True)
        self.addButton.setEnabled(True)

        number = len(self.contacts)
        self.nextButton.setEnabled(number > 1)
        self.previousButton.setEnabled(number > 1)

        self.submitButton.hide()
        self.cancelButton.hide()

    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.addressText.setText(self.oldAddress)

        if not self.contacts:
            self.nameLine.clear()
            self.addressText.clear()

        self.nameLine.setReadOnly(True)
        self.addressText.setReadOnly(True)
        self.addButton.setEnabled(True)

        number = len(self.contacts)
        self.nextButton.setEnabled(number > 1)
        self.previousButton.setEnabled(number > 1)

        self.submitButton.hide()
        self.cancelButton.hide()

    def next(self):
        name = self.nameLine.text()
        it = iter(self.contacts)

        try:
            while True:
                this_name, _ = it.next()
                if this_name == name:
                    next_name, next_address = it.next()
                    break
        except StopIteration:
            next_name, next_address = iter(self.contacts).next()

        self.nameLine.setText(next_name)
        self.addressText.setText(next_address)

    def previous(self):
        name = self.nameLine.text()
        prevname = prevaddr = None
        for this_name, this_address in self.contacts:
            if this_name == name:
                break

            prevname = this_name
            prevaddr = this_address
        else:
            self.nameLine.clear()
            self.addressText.clear()
            return

        if prevname is None:
            for prevname, prevaddr in self.contacts:
                pass

        self.nameLine.setText(prevname)
        self.addressText.setText(prevaddr)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addressBook = AddressBook()
    addressBook.show()
    sys.exit(app.exec())
