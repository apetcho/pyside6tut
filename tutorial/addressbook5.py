#!/usr/bin/env python3
from PySide6 import QtCore
from PySide6 import QtWidgets


class SortedDict(dict):
    class Iterator:
        def __ini__(self, sorted_dict: dict):
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

        self.contacts = SortedDict()
        self.oldName = ""
        self.oldAddress = ""
        self.currentMode = self.NavigationMode

        nameLabel = QtWidgets.QLabel("Name:")
        self.nameLine = QtWidgets.QLineEdit()
        self.nameLine.setReadOnly(True)

        addressLabel = QtWidgets.QLabel("Address:")
        self.addressText = QtWidgets.QTextEdit()
        self.addressText.setReadOnly(True)

        self.addButton = QtWidgets.QPushButton("&Add")
        self.editButton = QtWidgets.QPushButton("&Edit")
        self.editButton.setEnabled(False)
        self.removeButton = QtWidgets.QPushButton("&Remove")
        self.removeButton.setEnabled(False)
        self.findButton = QtWidgets.QPushButton("&Find")
        self.findButton.setEnabled(False)
        self.submitButton = QtWidgets.QPushButton("&Submit")
        self.submitButton.hide()
        self.cancelButton = QtWidgets.QPushButton("&Cancel")
        self.cancelButton.hide()

        self.nextButton = QtWidgets.QPushButton("&Next")
        self.nextButton.setEnabled(False)
        self.previousButton = QtWidgets.QPushButton("&Previous")
        self.previousButton.setEnabled(False)

        self.dialog = FindDialog()

        self.addButton.clicked.connect(self.addContact)
        self.submitButton.clicked.connect(self.submitContact)
        self.editButton.clicked.connect(self.editContact)
        self.removeButton.clicked.connect(self.removeContact)
        self.findButton.clicked.connect(self.findContact)
        self.cancelButton.clicked.connect(self.cancel)
        self.nextButton.clicked.connect(self.next)
        self.previousButton.clicked.connect(self.previous)

        buttonLayout1 = QtWidgets.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton)
        buttonLayout1.addWidget(self.editButton)
        buttonLayout1.addWidget(self.removeButton)
        buttonLayout1.addWidget(self.findButton)
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
        mainLayout.addLayout(buttonLayout2, 2, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.updateInterface(self.AddingMode)

    def editContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.updateInterface(self.EditingMode)

    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QtWidgets.QMessageBox.information(self, "Empty Field",
                "Please enter a name and address.")
            return

        if self.currentMode == self.AddingMode:
            if name not in self.contacts:
                self.contacts[name] = address
                QtWidgets.QMessageBox.information(self, "Add Successful",
                    f"{name!r} has been added to your address book.")
            else:
                QtWidgets.QMessageBox.information(self, "Add Unsuccessful",
                    f"Sorry, {name!r} is already in your address book.")
                return

        elif self.currentMode == self.EditingMode:
            if self.oldName != name:
                if name not in self.contacts:
                    QtWidgets.QMessageBox.information(self, "Edit Successful",
                        f"{self.oldAddress!r} has been edited in your address "
                        "book."
                    )
                    del self.contacts[self.oldName]
                    self.contacts[name] = address
                else:
                    QtWidgets.QMessageBox.information(self, "Edit Unsuccessful",
                        f"Sorry, {name!r} is already in your address book.")
                    return
            elif self.oldAddress != address:
                QtWidgets.QMessageBox.information(self, "Edit Successful",
                    f"{name!r} has been edited in your address book.")
                self.contacts[name] = address

        self.updateInterface(self.NavigationMode)

    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.addressText.setText(self.oldAddress)
        self.updateInterface(self.NavigationMode)

    def removeContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name in self.contacts:
            button = QtWidgets.QMessageBox.question(self, "Confirm Remove",
                f"Are you sure you want to remove {name!r}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if button == QtWidgets.QMessageBox.Yes:
                self.previous()
                del self.contacts[name]

                QtWidgets.QMessageBox.information(self, "Remove Successful",
                    f"{name!r} has been removed from your address book.")

        self.updateInterface(self.NavigationMode)

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

    def findContact(self):
        self.dialog.show()

        if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
            contactName = self.dialog.getFindText()

            if contactName in self.contacts:
                self.nameLine.setText(contactName)
                self.addressText.setText(self.contacts[contactName])
            else:
                QtWidgets.QMessageBox.information(self, "Contact Not Found",
                    f"Sorry, {contactName!r} is not in your address book.")
                return

        self.updateInterface(self.NavigationMode)

    def updateInterface(self, mode):
        self.currentMode = mode

        if self.currentMode in (self.AddingMode, self.EditingMode):
            self.nameLine.setReadOnly(False)
            self.nameLine.setFocus(QtCore.Qt.OtherFocusReason)
            self.addressText.setReadOnly(False)

            self.addButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)

            self.nextButton.setEnabled(False)
            self.previousButton.setEnabled(False)

            self.submitButton.show()
            self.cancelButton.show()

        elif self.currentMode == self.NavigationMode:
            if not self.contacts:
                self.nameLine.clear()
                self.addressText.clear()

            self.nameLine.setReadOnly(True)
            self.addressText.setReadOnly(True)
            self.addButton.setEnabled(True)

            number = len(self.contacts)
            self.editButton.setEnabled(number >= 1)
            self.removeButton.setEnabled(number >= 1)
            self.findButton.setEnabled(number > 2)
            self.nextButton.setEnabled(number > 1)
            self.previousButton.setEnabled(number > 1)

            self.submitButton.hide()
            self.cancelButton.hide()


class FindDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        findLabel = QtWidgets.QLabel("Enter the name of a contact:")
        self.lineEdit = QtWidgets.QLineEdit()

        self.findButton = QtWidgets.QPushButton("&Find")
        self.findText = ""

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(findLabel)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.findButton)

        self.setLayout(layout)
        self.setWindowTitle("Find a Contact")

        self.findButton.clicked.connect(self.findClicked)
        self.findButton.clicked.connect(self.accept)

    def findClicked(self):
        text = self.lineEdit.text()
        if not text:
            QtWidgets.QMessageBox.information(self, "Empty Field",
                "Please enter a name.")
            return
        else:
            self.findText = text
            self.lineEdit.clear()
            self.hide()

    def getFindText(self):
        return self.findText


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addressBook = AddressBook()
    addressBook.show()
    sys.exit(app.exec())
