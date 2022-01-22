#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class LCDRange(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LCDRange, self).__init__(parent)

        lcd = QtWidgets.QLCDNumber(2)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(0)
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)"))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(slider)
        self.setLayout(layout)


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"),
            qApp, QtCore.SLOT("quit()"))

        grid = QtWidgets.QGridLayout()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(quit)
        layout.addLayout(grid)
        self.setLayout(layout)
        for row in range(3):
            for column in range(3):
                grid.addWidget(LCDRange(), row, column)


app = QtWidgets.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec())
