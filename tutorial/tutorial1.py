#!/usr/bin/env python3
import sys
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
hello = QtWidgets.QPushButton("Hello World!")
hello.resize(100, 30)
hello.show()
sys.exit(app.exec())
