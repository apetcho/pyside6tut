#!/usr/bin/env python3
"""Tetrix

This is a Qt6 version of the classic Tetrix game.

The object of the game is to stack pieces dropped from the top of the playing
area so that they fill entire rows at the bottom of the playing area.

When a row is filled, all the blocks on that row are removed, the player earns
a number of points, and the peices above are moved down to occupy that row. If
more that one row is filled, the blocks on each row are removed, and the player
earns extra points.

The LEFT cursors cursor key moves the current piece one space to the left. the
RIGHT cursor key moves it one space to the right, the UP cursor key rotates the
piece counter-clockwise by 90 degrees, and the DOWN cursor key rotates the piece
clockwise by 90 degrees.

To avoid waiting for a piece to fall to the bottom of the board, press D to
immediately move the piece down by one row, or press the SPACE key to drop
it as close to the bottom of the board as possible.

This example example shows how a simple game can be created using only three
classes.

- The *TetrixWindow* class is used to display the payer's score, number of
lives, and information about the next piece to appear.
- The *TetrixBoard* class contains the next game logic, handles keyboard input,
and displays the pieces on the playing area.
- The *TetrixPiece* class contains information about each piece.

In this approach, the *TetrixBoard* clss is the most complex class, since it 
handle the game logic and rendering. One benefit of this is that the 
*TetrixWindow* and *TeTrixPiece* class are very simple and contains only a 
minimum of code.

Credit: Most of the code here is based on official PySide6 example of Tetrix 
code. 
Note: This code is used for learning Qt6 Programming.
"""
import random
from enum import IntEnum, auto
from unittest import result

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class ShapeEnum(IntEnum):
    NO_SHAPE = 0
    Z_SHAPE = 1
    S_SHAPE = 2
    LINE_SHAPE = 3
    T_SHAPE = 4
    SQUARE_SHAPE = 5
    L_SHAPE = 6
    MIRRORED_L_SHAPE = 7


class TetrixWindow(QtWidgets.QWidget):
    """TetrixWindow."""

    def __init__(self, root):
        super(TetrixWindow, self).__init__()

        self.board = TetrixBoard()

        nxtPieceLabel = QtWidgets.QLabel()
        nxtPieceLabel.setFrameStyle(
            QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        nxtPieceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.board.setNextPieceLabel(nxtPieceLabel)

        scoreLcd = QtWidgets.QLCDNumber(5)
        scoreLcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        levelLcd = QtWidgets.QLCDNumber(2)
        levelLcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        linesLcd = QtWidgets.QLCDNumber(5)
        linesLcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)

        startBtn = QtWidgets.QPushButton("&Start")
        startBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        quitBtn = QtWidgets.QPushButton("&Quit")
        quitBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        pauseBtn = QtWidgets.QPushButton("&Pause")
        pauseBtn.setFocusPolicy(QtCore.Qt.NoFocus)

        startBtn.clicked.connect(self.board.start)
        pauseBtn.clicked.connect(self.board.pause)
        quitBtn.clicked.connect(root.quit)
        self.board.scoreChanged.connect(scoreLcd.display)
        self.board.levelChanged.connect(levelLcd.display)
        self.board.linesRemovedChanged.connect(linesLcd.display)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.createLabel("NEXT"), 0, 0)
        layout.addWidget(nxtPieceLabel, 1, 0)
        layout.addWidget(self.createLabel("LEVEL"), 2, 0)
        layout.addWidget(levelLcd, 3, 0)
        layout.addWidget(startBtn, 4, 0)
        layout.addWidget(self.board, 0, 1, 6, 1)
        layout.addWidget(self.createLabel("SCORE"), 0, 2)
        layout.addWidget(scoreLcd, 1, 2)
        layout.addWidget(self.createLabel("LINES REMOVED"), 2, 2)
        layout.addWidget(linesLcd, 3, 2)
        layout.addWidget(quitBtn, 4, 2)
        layout.addWidget(pauseBtn, 5, 2)
        self.setLayout(layout)

        self.setWindowTitle("Tetrix")
        self.resize(550, 370)

    def createLabel(self, text):
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        return label


class TetrixBoard(QtWidgets.QFrame):
    """TetrixBoard."""
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22

    scoreChanged = QtCore.Signal(int)
    levelChanged = QtCore.Signal(int)
    linesRemovedChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(TetrixBoard, self).__init__(parent)

        self.timer = QtCore.QBasicTimer()
        self.nxtPieceLabel = None
        self.isWaitingAfterLine = False
        self.curPiece = TetrixPiece()
        self.nxtPiece = TetrixPiece()
        self.curx = 0
        self.cury = 0
        self.numLinesRemoved = 0
        self.numPiecesDropped = 0
        self.score = 0
        self.level = 0
        self.board = None

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

        self.nxtPiece.setRandomShape()

    def shapeAt(self, x, y):
        return self.board[(y * TetrixBoard.BOARD_WIDTH) + x]

    def setShapeAt(self, x, y, shape: ShapeEnum):
        self.board[(y * TetrixBoard.BOARD_WIDTH) + x] = shape

    def timeoutTime(self):
        return 1000 / (1 + self.level)

    def squareWidth(self):
        return self.contentsRect().width() / TetrixBoard.BOARD_WIDTH

    def squareHeight(self):
        return self.contentsRect().height() / TetrixBoard.BOARD_HEIGHT

    def setNextPieceLabel(self, label):
        self.nxtPieceLabel = label

    def sizeHint(self):
        return QtCore.QSize(TetrixBoard.BOARD_WIDTH * 15 + self.frameWidth()*2,
            TetrixBoard.BOARD_HEIGHT*15 + self.frameWidth()*2)

    def minimumSizeHint(self):
        return QtCore.QSize(TetrixBoard.BOARD_WIDTH*15 + self.frameWidth()*2,
            TetrixBoard.BOARD_WIDTH * 5 + self.frameWidth()*2)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.numPiecesDropped = 0
        self.score = 0
        self.level = 1
        self.clearBoard()

        self.linesRemovedChanged.emit(self.numLinesRemoved)
        self.scoreChanged.emit(self.score)
        self.levelChanged.emit(self.level)

        self.newPiece()
        self.timer.start(self.timeoutTime(), self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
        else:
            self.timer.start(self.timeoutTime(), self)

        self.update()

    def paintEvent(self, event):
        super(TetrixBoard, self).paintEvent(event)

        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        if self.isPaused:
            painter.drawText(rect, QtCore.Qt.AlignCenter, "Pause")
            return

        boardTop = rect.bottom() - TetrixBoard.BOARD_HEIGHT*self.squareHeight()
        for i in range(TetrixBoard.BOARD_HEIGHT):
            for j in range(TetrixBoard.BOARD_WIDTH):
                shape = self.shapeAt(j, TetrixBoard.BOARD_HEIGHT-i-1)
                if shape != ShapeEnum.NO_SHAPE:
                    self.drawSquare(
                        painter, rect().left() + j*self.squareWidth(),
                        boardTop+i*self.squareHeight(), shape)

        if self.curPiece.shape() != ShapeEnum.NO_SHAPE:
            for i in range(4):
                x = self.curx + self.curPiece.xcoord(i)
                y = self.cury - self.curPiece.ycoord(i)
                self.drawSquare(painter, rect.left() + x *self.squareWidth(),
                    boardTop+(TetrixBoard.BOARD_HEIGHT-y-1)*self.squareHeight(),
                    self.curPiece.shape())

    def keyPressEvent(self, event):
        if (not self.isStarted or self.isPaused or
            self.curPiece.shape() == ShapeEnum.NO_SHAPE):
            super(TetrixBoard, self).keyPressEvent(event)
            return

        key = event.key()
        if key == QtCore.Qt.Key_Left:
            self.tryMove(self.curPiece, self.curx-1, self.cury)
        elif key == QtCore.Qt.Key_Right:
            self.tryMove(self.curPiece, self.curx+1, self.cury)
        elif key == QtCore.Qt.Key_Down:
            self.tryMove(self.curPiece.rotatedRight(), self.curx, self.cury)
        elif key == QtCore.Qt.Key_Up:
            self.tryMove(self.curPiece.rotatedLeft(), self.curx, self.cury)
        elif key == QtCore.Qt.Key_Space:
            self.dropDown()
        elif key == QtCore.Qt.Key_D:
            self.oneLineDown()
        else:
            super(TetrixBoard, self).keyPressEvent(event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
                self.timer.start(self.timeoutTime(), self)
            else:
                self.oneLineDown()
        else:
            super(TetrixBoard, self).timerEvent(event)

    def clearBoard(self):
        self.board = [ShapeEnum.NO_SHAPE for i in 
            range(TetrixBoard.BOARD_HEIGHT*TetrixBoard.BOARD_WIDTH)]

    def dropDown(self):
        dropHeight = 0
        newy = self.cury
        while newy:
            if not self.tryMove(self.curPiece, self.cury, newy - 1):
                break
            newy -= 1
            dropHeight += 1

        self.pieceDropped(dropHeight)

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curx, self.cury-1):
            self.pieceDropped(0)

    def pieceDropped(self, dropHeight):
        for i in range(4):
            x = self.curx + self.curPiece.xcoord(i)
            y = self.cury - self.curPiece.ycoord(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.numPiecesDropped += 1
        if self.numPiecesDropped % 25 == 0:
            self.level += 1
            self.timer.start(self.timeoutTime(), self)
            self.levelChanged.emit(self.level)

        self.score += dropHeight + 7
        self.scoreChanged.emit(self.score)
        self.removeFullLines()

    def removeFullLines(self):
        numFullLines = 0
        for i in range(TetrixBoard.BOARD_HEIGHT -1, -1, -1):
            lineIsFull = True
            for j in range(TetrixBoard.BOARD_WIDTH):
                if self.shapeAt(j, i) == ShapeEnum.NO_SHAPE:
                    lineIsFull = False
                    break
            
            if lineIsFull:
                numFullLines += 1
                for k in range(TetrixBoard.BOARD_HEIGHT-1):
                    for j in range(TetrixBoard.BOARD_WIDTH):
                        self.setShapeAt(j, k, self.shapeAt(j, k+1))

                for j in range(TetrixBoard.BOARD_WIDTH):
                    self.setShapeAt(j, TetrixBoard.BOARD_HEIGHT-1,
                        ShapeEnum.NO_SHAPE)
        if numFullLines > 0:
            self.numLinesRemoved += numFullLines
            self.score += 10 * numFullLines
            self.linesRemovedChanged.emit(self.numLinesRemoved)
            self.scoreChanged.emit(self.score)

            self.timer.start(500, self)
            self.isWaitingAfterLine = True
            self.curPiece.setShape(ShapeEnum.NO_SHAPE)
            self.update()

    def newPiece(self):
        self.curPiece = self.nxtPiece
        self.nxtPiece.setRandomShape()
        self.showNextPiece()
        self.curx = (TetrixBoard.BOARD_WIDTH // 2) + 1
        self.cury = TetrixBoard.BOARD_HEIGHT - 1 + self.curPiece.ymin()

        if not self.tryMove(self.curPiece, self.curx, self.cury):
            self.curPiece.setShape(ShapeEnum.NO_SHAPE)
            self.timer.stop()
            self.isStarted = False

    def showNextPiece(self):
        if self.nxtPieceLabel is not None:
            return
        dx = self.nxtPiece.xmax() - self.nxtPiece.xmin() + 1
        dy = self.nxtPiece.ymax() - self.nxtPiece.ymin() + 1

        pixmap = QtGui.QPixmap(
            dx*self.squareWidth(), dy*self.squareHeight())
        painter = QtGui.QPainter(pixmap)
        painter.fillRect(
            pixmap.rect(), self.nxtPieceLabel.palette().background())

        for i in range(4):
            x = self.nxtPiece.xcoord(i) - self.nxtPiece.xmin()
            y = self.nxtPiece.ycoord(i) - self.nxtPiece.ymin()
            self.drawSquare(painter, x*self.squareWidth(),
                y*self.squareHeight(), self.nxtPiece.shape())

        self.nxtPieceLabel.setPixmap(pixmap)    # FIXME

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.xcoord(i)
            y = newY - newPiece.ycoord(i)
            if (x < 0 or x >= TetrixBoard.BOARD_WIDTH or y < 0 or
                y >= TetrixBoard.BOARD_HEIGHT):
                return False
            if self.shapeAt(x, y) != ShapeEnum.NO_SHAPE:
                return False

        self.curPiece = newPiece
        self.curx = newX
        self.cury = newY
        self.update()
        return True

    def drawSquare(self, painter: QtGui.QPainter, x, y, shape: ShapeEnum):
        COLOR_TABLE = [
            0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
            0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00
        ]
        color = QtGui.QColor(COLOR_TABLE[shape.value])
        painter.fillRect(x+1, y+1, self.squareWidth()-2,
            self.squareHeight()-2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y+self.squareHeight()-1, x, y)
        painter.drawLine(x, y, x+self.squareWidth()-1, y)

        painter.setPen(color.darker())
        painter.drawLine(x+1, y+self.squareHeight()-1,
            x+self.squareWidth()-1, y+self.squareHeight()-1)
        painter.drawLine(x+self.squareWidth()-1, y+self.squareHeight()-1,
            x+self.squareWidth()-1, y+1)

class TetrixPiece:

    COORDS_TABLES = (
        ((0,   0), (0,  0), (0,  0), ( 0, 0)),
        ((0,  -1), (0,  0), (-1, 0), (-1, 1)),
        ((0,  -1), (0,  0), ( 1, 0), ( 1, 1)),
        ((0,  -1), (0,  0), ( 0, 1), ( 0, 2)),
        ((-1,  0), (0,  0), ( 1, 0), ( 0, 1)),
        (( 0,  0), (1,  0), ( 0, 1), ( 1, 1)),
        ((-1, -1), (0, -1), ( 0, 0), ( 0, 1)),
        (( 1, -1), (0, -1), ( 0, 0), ( 0, 1))
    )

    def __init__(self):
        self.coords = [[0, 0] for _ in range(4)]
        self.pieceShape = ShapeEnum.NO_SHAPE
        self.setShape(ShapeEnum.NO_SHAPE)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape: ShapeEnum):
        table = TetrixPiece.COORDS_TABLES[shape.value]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        SHAPES = [
            ShapeEnum.L_SHAPE, ShapeEnum.LINE_SHAPE, ShapeEnum.MIRRORED_L_SHAPE,
            ShapeEnum.S_SHAPE, ShapeEnum.SQUARE_SHAPE, ShapeEnum.T_SHAPE,
            ShapeEnum.Z_SHAPE
        ]
        shape = random.choice(SHAPES)
        self.setShape(shape)

    def xcoord(self, index):
        return self.coords[index][0]

    def ycoord(self, index):
        return self.coords[index][1]

    def setXCoord(self, index, x):
        self.coords[index][0] = x

    def setYCoord(self, index, y):
        self.coords[index][1] = y

    def xmin(self):
        vmin = self.coords[0][0]
        for i in range(4):
            vmin = min(vmin, self.coords[i][0])
        return vmin

    def xmax(self):
        vmax = self.coords[0][0]
        for i in range(4):
            vmax = max(vmax, self.coords[i][0])
        return vmax

    def ymin(self):
        vmin = self.coords[0][1]
        for i in range(4):
            vmin = min(vmin, self.coords[i][1])
        return vmin

    def ymax(self):
        vmax = self.coords[0][1]
        for i in range(4):
            vmax = max(vmax, self.coords[i][1])
        return vmax

    def rotatedLeft(self):
        if self.pieceShape == ShapeEnum.SQUARE_SHAPE:
            return self

        result = TetrixPiece()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setXCoord(i, self.ycoord(i))
            result.setYCoord(i, -self.xcoord(i))
        return result

    def rotatedRight(self):
        if self.pieceShape == ShapeEnum.SQUARE_SHAPE:
            return self

        result = TetrixPiece()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setXCoord(i, -self.ycoord(i))
            result.setYCoord(i, self.xcoord(i))
        return result


if __name__ == "__main__":
    import sys
    import time

    app = QtWidgets.QApplication(sys.argv)
    tetrix = TetrixWindow()
    tetrix.show()
    random.seed(time.time())
    sys.exit(app.exec())
