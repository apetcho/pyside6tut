#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(QtWidgets, self).__init__(parent)
        # TODO

    def value(self):
        pass

    @QtCore.Slot(int)
    def setValue(self, value):
        pass


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        # TODO


widget = MyWidget()
widget.show()
sys.exit(app.exec())
