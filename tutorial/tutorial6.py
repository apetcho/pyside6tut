#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class LCDRange(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LCDRange, self).__init__(parent)
        # TODO


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        # TODO


app = QtWidgets.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec())
