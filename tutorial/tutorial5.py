#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        lcd = QtWidgets.QLCDNumber(2)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(0)

        self.connect(quit, QtCore.SIGNAL("clicked()"),
            app, QtCore.SLOT("quit()"))
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)"))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(quit)
        layout.addWidget(lcd)
        layout.addWidget(slider)
        self.setLayout(layout)



widget = MyWidget()
widget.show()
sys.exit(app.exec())
