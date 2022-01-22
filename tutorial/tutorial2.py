#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

quit = QtWidgets.QPushButton("Quit")
quit.resize(75, 30)
quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
QtCore.QObject.connect(
    quit, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()")
)

quit.show()
sys.exit(app.exec())
