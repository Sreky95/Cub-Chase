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
        self.lives = 3

        if self.playernumber == 1:
            temp = QPixmap("./Pictures/Player1Down.png")
        else:
            if self.playernumber == 2:
                temp = QPixmap("./Pictures/Player2Down.png")

        self.setPixmap(temp.scaled(40, 40))
        self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)

    def moveup(self):

        if not self.stunned:
            if self.playernumber == 1:
                temp = QPixmap("./Pictures/Player1Up.png")
            else:
                if self.playernumber == 2:
                    temp = QPixmap("./Pictures/Player2Up.png")

            self.setPixmap(temp.scaled(40, 40))
            if self.TerrainMatrix[self.x - 1][self.y].terraintype > 0:
                self.x -= 1
                self.checktile()
                self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)

    def moveleft(self):

        if not self.stunned:
            if self.playernumber == 1:
                temp = QPixmap("./Pictures/Player1Left.png")
            else:
                if self.playernumber == 2:
                    temp = QPixmap("./Pictures/Player2Left.png")

            self.setPixmap(temp.scaled(40, 40))
            if self.TerrainMatrix[self.x][self.y - 1].terraintype > 0:
                self.y -= 1
                self.checktile()
                self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)

    def moveright(self):

        if not self.stunned:
            if self.playernumber == 1:
                temp = QPixmap("./Pictures/Player1Right.png")
            else:
                if self.playernumber == 2:
                    temp = QPixmap("./Pictures/Player2Right.png")

            self.setPixmap(temp.scaled(40, 40))
            if self.TerrainMatrix[self.x][self.y + 1].terraintype > 0:
                self.y += 1
                self.checktile()
                self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)

    def movedown(self):

        if not self.stunned:
            if self.playernumber == 1:
                temp = QPixmap("./Pictures/Player1Down.png")
            else:
                if self.playernumber == 2:
                    temp = QPixmap("./Pictures/Player2Down.png")

            self.setPixmap(temp.scaled(40, 40))
            if self.TerrainMatrix[self.x + 1][self.y].terraintype > 0:
                self.x += 1
                self.checktile()
                self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)

    def unstun(self):

        self.stunned = False
        self.parentGameWindow.layout.deleteTrap((self.y) * len(self.TerrainMatrix[0]) + self.x,
                self.TerrainMatrix[self.x][self.y].terraintype)

    def kill(self):

        if self.lives > 0:
            self.x = math.floor(len(self.TerrainMatrix) / 2)
            self.y = math.floor(len(self.TerrainMatrix[0]) / 2)
            self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)
            self.lives -= 1
            self.removelife()
        else:
            temp = QPixmap("./Pictures/Nothing.png")
            self.setPixmap(temp.scaled(40, 40))
            self.stunned = True
            self.x = math.floor(len(self.TerrainMatrix) / 2)
            self.y = math.floor(len(self.TerrainMatrix[0]) / 2)
            self.setGeometry((self.y * 40) + 11, (self.x * 40) + 11, 40, 40)

    def removelife(self):

        temp = QPixmap("./Pictures/Nothing.png")
        if self.playernumber == 1:
            if self.lives == 2:
                self.parentGameWindow.player1hp3.setPixmap(temp)
            else:
                if self.lives == 1:
                    self.parentGameWindow.player1hp2.setPixmap(temp)
                else:
                    if self.lives == 0:
                        self.parentGameWindow.player1hp1.setPixmap(temp)
        else:
            if self.playernumber == 2:
                if self.lives == 2:
                    self.parentGameWindow.player2hp3.setPixmap(temp)
                else:
                    if self.lives == 1:
                        self.parentGameWindow.player2hp2.setPixmap(temp)
                    else:
                        if self.lives == 0:
                            self.parentGameWindow.player2hp1.setPixmap(temp)

    def checktile(self):

        self.checkprints()
        self.checktrap()
        self.checknpc()

    def checknpc(self):

        if (self.parentGameWindow.NPC1.x == self.x and self.parentGameWindow.NPC1.y == self.y) or \
                (self.parentGameWindow.NPC2.x == self.x and self.parentGameWindow.NPC2.y == self.y) or \
                (self.parentGameWindow.NPC3.x == self.x and self.parentGameWindow.NPC3.y == self.y) or \
                (self.parentGameWindow.NPC4.x == self.x and self.parentGameWindow.NPC4.y == self.y):
            self.kill()

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

    def checkend(self):

        None                #Logika za kraj



