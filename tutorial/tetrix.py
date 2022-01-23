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

    def __init__(self):
        super(TetrixWindow, self).__init__()

        # TODO

    def createLabel(self, text):
        pass


class TetrixBoard(QtWidgets.QFrame):

    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22

    scoreChanged = QtCore.Signal(int)
    levelChanged = QtCore.Signal(int)
    linesRemovedChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(TetrixBoard, self).__init__(parent)

        # TODO

    def shapeAt(self, x, y):
        pass

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
