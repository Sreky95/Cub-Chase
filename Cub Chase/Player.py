from PyQt5.QtWidgets import (QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QGridLayout,
                             QVBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QObject, Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap, QKeyEvent
import sys, random, math, threading, time, multiprocessing


class Player(QLabel):

    def __init__(self, parent, number):

        self.parentGameWindow = parent
        super().__init__(self.parentGameWindow)
        self.TerrainMatrix = self.parentGameWindow.layout.TerrainMatrix
        self.x = math.floor(len(self.TerrainMatrix) / 2)
        self.y = math.floor(len(self.TerrainMatrix[0]) / 2)
        self.playernumber = number
        #self.available = [False, False, False, False]

        if self.playernumber == 1:
            self.Model = QPixmap("./Pictures/Player1.png")
        else:
            self.Model = QPixmap("./Pictures/Player2.png")

        self.setPixmap(self.Model.scaled(30, 30))
        self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)