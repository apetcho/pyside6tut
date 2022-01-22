#!/usr/bin/env python3
import pickle
from sre_parse import _OpGroupRefExistsType
from tkinter import mainloop
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

        self.loadButton = QtWidgets.QPushButton("&Load...")
        self.loadButton.setToolTip("Load contacts from a file")
        self.saveButton = QtWidgets.QPushButton("Sa&ve...")
        self.saveButton.setToolTip("Save contacts to a file")
        self.saveButton.setEnabled(False)

        self.exportButton = QtWidgets.QPushButton("Ex&port")
        self.exportButton.setToolTip("Export as vCard")
        self.exportButton.setEnabled(False)

        self.dialog = FindDialog()

        self.addButton.clicked.connect(self.addContact)
        self.submitButton.clicked.connect(self.submitContact)
        self.editButton.clicked.connect(self.editContact)
        self.removeButton.clicked.connect(self.removeContact)
        self.findButton.clicked.connect(self.findContact)
        self.cancelButton.clicked.connect(self.cancel)
        self.nextButton.clicked.connect(self.next)
        self.previousButton.clicked.connect(self.previous)
        self.loadButton.clicked.connect(self.loadFromFile)
        self.saveButton.clicked.connect(self.saveToFile)
        self.exportButton.clicked.connect(self.exportAsVCard)

        buttonLayout1 = QtWidgets.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton)
        buttonLayout1.addWidget(self.editButton)
        buttonLayout1.addWidget(self.removeButton)
        buttonLayout1.addWidget(self.findButton)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addWidget(self.loadButton)
        buttonLayout1.addWidget(self.saveButton)
        buttonLayout1.addWidget(self.exportButton)
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
                        f"{self.oldName!r} has been edited in your address "
                        "book.")
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
        addres = self.addressText.toPlainText()

        if name in self.contacts:
            button = QtWidgets.QMessageBox.question(self, "Confirm Remove",
                "Are you sure you want to remove {name!r}?",
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
                _name, _ = it.next()
                if _name == name:
                    _name, _addr = it.next()
                    break
        except StopIteration:
            _name, _addr = iter(self.contacts).next()

        self.nameLine.setText(_name)
        self.addressText.setText(_addr)

    def previous(self):
        name = self.nameLine.text()
        prevname = prevaddr = None
        for _name, _addr in self.contacts:
            if _name == name:
                break
            prevname = _name
            prevaddr = _addr
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
                    f"Sorry {contactName!r} is not in your address book.")
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

            self.loadButton.setEnabled(False)
            self.saveButton.setEnabled(False)
            self.exportButton.setEnabled(False)

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

            self.exportButton.setEnabled(number >= 1)

            self.loadButton.setEnabled(True)
            self.saveButton.setEnabled(number >= 1)

    def saveToFile(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self,
            "Save Address Book", "",
            "Address Book (*.abk);;All Files (*)")
        if not fname:
            return

        try:
            oufile = open(str(fname), "wb")
        except IOError:
            QtWidgets.QMessageBox.information(self, "Unable to open file",
                "There was an error opening {fname!r}")
            return

        pickle.dump(self.contacts, oufile)
        oufile.close()

    def loadFromFile(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Address Book", "",
            "Address Book (*.abk);;All Files (*)")
        if not fname:
            return

        try:
            infile = open(str(fname), "rb")
        except IOError:
            QtWidgets.QMessageBox.information(
                self, "Unable to open file",
                f"There was an error opening {fname!r}")
            return

        self.contacts = pickle.load(infile)
        infile.close()
        if len(self.contacts) == 0:
            QtWidgets.QMessageBox.information(
                self, "No contacts in file",
                "The file you are attempting to open contains no contacts.")
        else:
            for name, addr in self.contacts:
                self.nameLine.setText(name)
                self.addressText.setText(addr)

        self.updateInterface(self.NavigationMode)

    def exportAsVCard(self):
        name = str(self.nameLine.text())
        address = self.addressText.toPlainText()

        nameList = name.split()

        if len(nameList) > 1:
            firstName = nameList[0]
            lastName = nameList[1]
        else:
            firstName = name
            lastName = ""

        fileName = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Contact", "",
            "vCard Files (*.vcf);;All Files (*)")[0]

        if not fileName:
            return

        outfile = QtCore.QFile(fileName)
        if not outfile.open(QtCore.QIODevice.WriteOnly):
            QtWidgets.QMessageBox.information(
                self, "Unable to open file", outfile.errorString())
            return
        
        outstr = QtCore.QTextStream(outfile)

        outstr << "BEGIN::VCARD" << "\n"
        outstr << "VERSION:2.1"  << "\n"
        outstr << "N:" << lastName << ";" << firstName << "\n"
        outstr << "FN:" << " ".join(nameList) << "\n"

        address.replace(";", "\\;")
        address.replace("\n", ";")
        address.replace(",", " ")

        outstr << "ADR;HOME:;" << address << "\n"
        outstr << "END:VCARD" << "\n"

        QtWidgets.QMessageBox.information(
            self, "Export Successful",
            f"{name!r} has been exported as a vCard.")


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
        self.windowTitle("Find a Contact")

        self.findButton.clicked.connect(self.findClicked)
        self.findButton.clicked.connect(self.accept)

    def findClicked(self):
        text = self.lineEdit.text()
        if not text:
            QtWidgets.QMessageBox.information(
                self, "Empty Field", "Please enter a name.")
            return
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
