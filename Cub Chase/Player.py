from PyQt5.QtWidgets import (QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QGridLayout,
                             QVBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QObject, Qt, QTimer
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
        self.stunned = False
        self.timer = None

        if self.playernumber == 1:
            temp = QPixmap("./Pictures/Player1Down.png")
        else:
            if self.playernumber == 2:
                temp = QPixmap("./Pictures/Player2Down.png")

        self.setPixmap(temp.scaled(30, 30))
        self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)

    def moveup(self):

        if self.playernumber == 1:
            temp = QPixmap("./Pictures/Player1Up.png")
        else:
            if self.playernumber == 2:
                temp = QPixmap("./Pictures/Player2Up.png")

        self.setPixmap(temp.scaled(30, 30))

        if not self.stunned:
            if self.TerrainMatrix[self.x - 1][self.y].terraintype > 0:
                self.x -= 1
                self.checktile()
                self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)

    def moveleft(self):

        if self.playernumber == 1:
            temp = QPixmap("./Pictures/Player1Left.png")
        else:
            if self.playernumber == 2:
                temp = QPixmap("./Pictures/Player2Left.png")

        self.setPixmap(temp.scaled(30, 30))

        if not self.stunned:
            if self.TerrainMatrix[self.x][self.y - 1].terraintype > 0:
                self.y -= 1
                self.checktile()
                self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)

    def moveright(self):

        if self.playernumber == 1:
            temp = QPixmap("./Pictures/Player1Right.png")
        else:
            if self.playernumber == 2:
                temp = QPixmap("./Pictures/Player2Right.png")

        self.setPixmap(temp.scaled(30, 30))

        if not self.stunned:
            if self.TerrainMatrix[self.x][self.y + 1].terraintype > 0:
                self.y += 1
                self.checktile()
                self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)

    def movedown(self):

        if self.playernumber == 1:
            temp = QPixmap("./Pictures/Player1Down.png")
        else:
            if self.playernumber == 2:
                temp = QPixmap("./Pictures/Player2Down.png")

        self.setPixmap(temp.scaled(30, 30))

        if not self.stunned:
            if self.TerrainMatrix[self.x + 1][self.y].terraintype > 0:
                self.x += 1
                self.checktile()
                self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)

    def unstun(self):

        self.stunned = False
        self.parentGameWindow.layout.deleteTrap((self.y) * len(self.TerrainMatrix[0]) + self.x,
                self.TerrainMatrix[self.x][self.y].terraintype)

    def checktile(self):

        self.checkprints()
        self.checktrap()
        self.checknpc()

    def checknpc(self):

        None
        #check if there is an NPC in this tile

    def checktrap(self):

        if self.TerrainMatrix[self.x][self.y].trap > 0:
            if self.TerrainMatrix[self.x][self.y].trap == 10:
                self.TerrainMatrix[self.x][self.y].trap = self.playernumber
                self.parentGameWindow.layout.activateTrap((self.y) * len(self.TerrainMatrix[0]) + self.x,
                    self.playernumber, self.TerrainMatrix[self.x][self.y].terraintype)
            else:
                if self.TerrainMatrix[self.x][self.y].trap != self.playernumber:
                    self.TerrainMatrix[self.x][self.y].trap = 0
                    self.stunned = True
                    self.timer = QTimer()
                    self.timer.setSingleShot(True)
                    self.timer.timeout.connect(self.unstun)
                    self.timer.start(5000)

    def checkprints(self):

        if self.TerrainMatrix[self.x][self.y].terraintype == 1:
            if self.TerrainMatrix[self.x][self.y].footprints == 0:
                self.TerrainMatrix[self.x][self.y].footprints = self.playernumber
                self.parentGameWindow.layout.replacePrints\
                    ((self.y) * len(self.TerrainMatrix[0]) + self.x, self.playernumber)



