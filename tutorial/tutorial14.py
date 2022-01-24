#!/usr/bin/env python3
import sys
import math
import random
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, text=None, parent=None):
        if isinstance(text, QtWidgets.QWidget):
            parent = text
            text = None
        super(LCDRange, self).__init__(parent)

        self.init()
        if text:
            self.setText(text)

    def init(self):
        lcd = QtWidgets.QLCDNumber(2)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.Alignment | QtCore.Qt.AlignTop)
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred | QtWidgets.QSizePolicy.Fixed)

        self.connect(
            self.slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)")
        )
        self.connect(
            self.slider, QtCore.SIGNAL("valueChanged(int)"),
            self, QtCore.SIGNAL("valueChanged(int)")
        )
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        self.slider.setValue(value)

    def text(self):
        return self.label.text()

    def setRange(self, vmin, vmax):
        if vmin < 0 or vmax > 99 or vmin > vmax:
            QtCore.qWarning(
                f"LCDRange::setRange({vmin:d}, {vmax:d})\n"
                "\tRange must be 0..99\n"
                "\tand vmin must not be greater than vmax"
            )
            return
        self.slider.setRange(vmin, vmax)

    def setText(self, text):
        self.label.setText(text)


class CannonField(QtWidgets.QWidget):

    angleChanged = QtCore.Signal(int)
    forceChanged = QtCore.Signal(int)
    hit = QtCore.Signal()
    missed = QtCore.Signal()
    canShoot = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(CannonField, self).__init__(parent)

        self.currentAngle = 45
        self.currentForce = 0
        self.timerCount = 0
        self.autoShootTimer = QtCore.QTimer(self)
        self.connect(
            self.autoShootTimer, QtCore.SIGNAL("timeout()"), self.moveShot
        )
        self.shootAngle = 0
        self.shootForce = 0
        self.target = QtCore.QPoint(0, 0)
        self.gameEnded = False
        self.barrelPressed = False
        self.setPalette(QtGui.QPalette(QtGui.QColor(2550, 250, 200)))
        self.setAutoFillBackground(True)
        self.newTarget()

    def angle(self):
        return self.currentAngle

    @QtCore.Slot(int)
    def setAngle(self, angle):
        angle = 5 if angle < 5 else angle
        angle = 85 if angle > 85 else angle
        if self.currentAngle == angle:
            return
        self.currentAngle = angle
        self.update()
        self.emit(QtCore.SIGNAL("angleChanged(int)"), self.currentAngle)

    def force(self):
        return self.currentForce

    @QtCore.Slot(int)
    def setForce(self, frc):
        frc = 0 if frc < 0 else frc
        if self.currentForce == frc:
            return
        self.currentForce = frc
        self.emit(QtCore.SIGNAL("forceChanged(int)"), self.currentForce)

    @QtCore.Slot()
    def shoot(self):
        if self.isShooting():
            return
        self.timerCount = 0
        self.shootAngle = self.currentAngle
        self.shootForce = self.currentForce
        self.autoShootTimer.start(5)
        self.emit(QtCore.SIGNAL("canShoot(bool)"), False)

    firstTime = True

    def newTarget(self):
        if CannonField.firstTime:
            CannonField.firstTime = False
            midnight = QtCore.QTime(0, 0, 0)
            random.seed(midnight.secsTo(QtCore.QTime.currentTime()))

        self.target = QtCore.QPoint(
            200 + random.randint(0, 190-1),
             10 + random.randint(0, 255-1)
        )
        self.update()

    def setGameOver(self):
        if self.gameEnded:
            return
        if self.isShooting():
            self.autoShootTimer.stop()
        self.gameEnded = True
        self.update()

    def restartGame(self):
        if self.isShooting():
            self.autoShootTimer.stop()
        self.gameEnded = False
        self.update()
        self.emit(QtCore.SIGNAL("canShoot(bool)"), True)

    @QtCore.Slot()
    def moveShot(self):
        region = QtGui.QRegion(self.shotRect())
        self.timerCount += 1

        shotR = self.shotRect()

        if shotR.intersects(self.targetRect()):
            self.autoShootTimer.stop()
            self.emit(QtCore.SIGNAL("hit()"))
            self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        elif (shotR.x() > self.width() or shotR.y() > self.height() or
             shotR.intersects(self.barrierRect())):
             self.autoShootTimer.stop()
             self.emit(QtCore.SIGNAL("missed()"))
             self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        else:
            region = region.united(QtGui.QRegion(shotR))

        self.update(region)

    def mousePressEvent(self, event: QtCore.QEvent):
        if event.button() != QtCore.Qt.LeftButton:
            return
        if self.barrelHit(event.position().toPoint()):
            self.barrelPressed = True

    def mouseMoveEvent(self, event: QtCore.QEvent):
        if not self.barrelPressed:
            return
        pos = event.position().toPoint()
        if pos.x() <= 0:
            pos.setX(1)
        if pos.y() >= self.height():
            pos.setY(self.height()-1)
        rad = math.atan((float(self.rect().bottom()) - pos.y())/pos.x())
        self.setAngle(round(rad * 180 / math.pi))

    def mouseReleaseEvent(self, event: QtCore.QEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.barrelPressed = False

    def paintEvent(self, event: QtCore.QEvent):
        painter = QtGui.QPainter(self)

        if self.gameEnded:
            painter.setPen(QtCore.Qt.black)
            painter.setFont(QtGui.QFont("Courier", 48, QtGui.QFont.Bold))
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Game Over")

        self.paintCannon(painter)
        self.paintBarrier(painter)
        if self.isShooting():
            self.paintShot(painter)
        if not self.gameEnded:
            self.painterTarget(painter)

    def paintShot(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.shotRect())

    def painterTarget(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(self.targetRect())

    def paintBarrier(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.yellow)
        painter.drawRect(self.barrierRect())

    barrelRect = QtCore.QRect(33, -4, 15, 8)

    def paintCannon(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.blue)

        painter.save()
        painter.translate(0, self.height())
        painter.drawPie(QtCore.QRect(-35, -35, 70, 70), 0, 90*16)
        painter.rotate(-self.currentAngle)
        painter.drawRect(CannonField.barrelRect)
        painter.restore()

    def cannonRect(self):
        result = QtCore.QRect(0, 0, 50, 50)
        result.moveBottomLeft(self.rect().bottomLect())
        return result

    def shotRect(self):
        gravity = 9.8   # XXX
        t = self.timerCount / 40.0
        velocity = self.shootForce
        angle = self.shootAngle * math.pi / 180

        vx = velocity * math.cos(angle)
        vy = velocity * math.sin(angle)
        x0 = (CannonField.barrelRect.right()+5)*math.cos(angle)
        y0 = (CannonField.barrelRect.right()+5)*math.sin(angle)

        x = x0 + vx*t
        y = y0 + vy*t -0.5*gravity*t*t 

        result = QtCore.QRect(0, 0, 6, 6)
        result.moveCenter(
            QtCore.QPoint(round(x), self.height()-1-round(y))
        )
        return result

    def targetRect(self):
        result = QtCore.QRect(0, 0, 20, 10)
        result.moveCenter(
            QtCore.QPoint(self.target.x(), self.height()-1-self.target.y())
        )
        return result

    def barrierRect(self):
        return QtCore.QRect(145, self.height()-100, 15, 99)

    def barrelHit(self, pos):
        matrix = QtGui.QTransform()
        matrix.translate(0, self.height())
        matrix.rotate(-self.currentAngle)
        matrix, invertible = matrix.inverted()
        return self.barrelRect.contains(matrix.map(pos))

    def gameOver(self):
        return self.gameEnded

    def isShooting(self):
        return self.autoShootTimer.isActive()

    def sizeHint(self):
        return QtCore.QSize(400, 300)


class GameBoard(QtWidgets.QWidget):

    def __init__(self, root, parent=None):
        super(GameBoard, self).__init__(parent)

        quit = QtWidgets.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(
            quit, QtCore.SIGNAL("clicked()"),
            root, QtCore.SLOT("quit()")
        )

        angle = LCDRange("ANGLE")
        angle.setRange(5, 85)

        frc = LCDRange("FORCE")
        frc.setRange(10, 50)

        cannonBox = QtWidgets.QFrame()
        cannonBox.setFrameStyle(
            QtWidgets.QFrame.WinPanel | QtWidgets.QFrame.Sunken
        )
        self.cannonField = CannonField()

        # --
        self.connect(
            angle, QtCore.SIGNAL("valueChanged(int)"),
            self.cannonField.setAngle
        )
        self.connect(
            self.cannonField, QtCore.SIGNAL("angleChanged(int)"),
            angle.setValue
        )
        self.connect(
            frc, QtCore.SIGNAL("valueChanged(int)"),
            self.cannonField.setForce
        )
        self.connect(
            self.cannonField, QtCore.SIGNAL("forceChanged(int)"),
            frc.setValue
        )
        self.connect(self.cannonField, QtCore.SIGNAL("hit()", self.hit))
        self.connect(self.cannonField, QtCore.SIGNAL("missed()"), self.missed)

        shoot = QtWidgets.QPushButton("&Shoot")
        shoot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(shoot, QtCore.SIGNAL("clicked()"), self.fire)
        self.connect(
            self.cannonField, QtCore.SIGNAL("canShoot(bool)"),
            shoot, QtCore.SLOT("setEnabled(bool)")
        )

        restart = QtWidgets.QPushButton("&New Game")
        restart.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(restart, QtCore.SIGNAL("clicked()"), self.newGame)

        self.hits = QtWidgets.QLCDNumber(2)
        self.shotsLeft = QtWidgets.QLCDNumber(2)
        hitsLabel = QtWidgets.QLabel("HITS")
        shotsLeftLabel = QtWidgets.QLabel("SHOTS LEFT")

        QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Enter),
            self, self.fire
        )
        QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self, self.fire
        )
        QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Q),
            self, QtCore.SLOT("close()")
        )

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(shoot)
        topLayout.addWidget(self.hits)
        topLayout.addWidget(hitsLabel)
        topLayout.addWidget(self.shotsLeft)
        topLayout.addWidget(shotsLeftLabel)
        topLayout.addStretch(1)
        topLayout.addWidget(restart)

        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addWidget(angle)
        leftLayout.addWidget(frc)

        cannonLayout = QtWidgets.QVBoxLayout()
        cannonLayout.addWidget(self.cannonField)
        cannonBox.setLayout(cannonLayout)

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addLayout(topLayout, 0, 1)
        gridLayout.addLayout(leftLayout, 1, 0)
        gridLayout.addWidget(cannonBox, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        angle.setValue(60)
        frc.setValue(25)
        angle.setFocus()

    @QtCore.Slot()
    def fire(self):
        if self.cannonField.gameOver() or self.cannonField.isShooting():
            return
        self.shotsLeft.display(self.shotsLeft.intValue()-1)
        self.cannonField.shoot()

    @QtCore.Slot()
    def hit(self):
        self.hits.display(self.hits.intValue()+1)
        if self.shotsLeft.intValue() == 0:
            self.cannonField.setGameOver()
        else:
            self.cannonField.newTarget()

    @QtCore.Slot()
    def missed(self):
        if self.shotsLeft.intValue() == 0:
            self.cannonField.setGameOver()

    @QtCore.Slot()
    def newGame(self):
        self.shotsLeft.display(15)
        self.hits.display(0)
        self.cannonField.restartGame()
        self.cannonField.newTarget()

def main():
    pass


main()
