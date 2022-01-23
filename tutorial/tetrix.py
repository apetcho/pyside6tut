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
        pass

    def timeoutTime(self):
        pass

    def squareWidth(self):
        pass

    def squareHeight(self):
        pass

    def setNextPieceLabel(self, lable):
        pass

    def sizeHint(self):
        pass

    def minimumSizeHint(self):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def paintEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass

    def timerEvent(self, event):
        pass

    def clearBoard(self):
        pass

    def dropDown(self):
        pass

    def oneLineDown(self):
        pass

    def pieceDropped(self):
        pass

    def removeFullLines(self):
        pass

    def newPiece(self):
        pass

    def showNextPiece(self):
        pass

    def tryMove(self, newPiece, newX, newY):
        pass

    def drawSquare(self, painter, x, y, shape: ShapeEnum):
        pass


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
        pass

    def shape(self):
        pass

    def setShape(self, shape: ShapeEnum):
        pass

    def setRandomShape(self):
        pass

    def xcoord(self, index):
        pass

    def ycoord(self, index):
        pass

    def setXCoord(self, index, x):
        pass

    def setYCoord(self, index, y):
        pass

    def xmin(self):
        pass

    def xmax(self):
        pass

    def ymin(self):
        pass

    def ymax(self):
        pass

    def rotatedLeft(self):
        pass

    def rotatedRight(self):
        pass


if __name__ == "__main__":
    import sys
    import time

    app = QtWidgets.QApplication(sys.argv)
    tetrix = TetrixWindow()
    tetrix.show()
    random.seed(time.time())
    sys.exit(app.exec())
