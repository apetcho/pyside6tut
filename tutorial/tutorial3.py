#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QWidget()
window.resize(200, 120)

quit = QtWidgets.QPushButton("Quit", window)
quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
quit.setGeometry(10, 40, 180, 40)
QtCore.QObject.connect(
    quit, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()")
)

window.show()
sys.exit(app.exec())
