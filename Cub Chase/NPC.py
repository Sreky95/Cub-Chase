from PyQt5.QtWidgets import (QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QGridLayout,
                             QVBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap
import sys, random, math, threading, time


class NPC(QLabel):

    def __init__(self, parent):

        super().__init__(parent)
        self.terrain = parent.layout.TerrainMatrix
        self.x = 0
        self.y = 0
        self.spawned = False
        self.passableMatrix = None

        self.spawn()

        self.model = QPixmap("./Pictures/Enemy.png")
        self.setPixmap(self.model.scaled(30, 30))
        self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)

    def spawn(self):

        self.passableMatrix = [[" " for x in range(len(self.terrain))] for y in range(len(self.terrain[0]))]
        for y in range(len(self.terrain)):
            for x in range(len(self.terrain[y])):
                self.passableMatrix[x][y] = str(self.terrain[x][y].passable)

        while not self.spawned:
            x = random.randint(1, len(self.terrain[0]) - 1)
            y = random.randint(1, len(self.terrain) - 1)
            if self.passableMatrix[x][y] == "True":
                self.x = x
                self.y = y
                self.spawned = True

    def __update_position__(self, position):

        self.setGeometry((position[1] * 40) + 16, (position[0] * 40) + 16, 30, 30)


class NPCMovement(object):

    def __init__(self, piper):

        self.piper = piper
        self.pipes = piper.recv()
        self.terrain = piper.recv()
        self.x = piper.recv()
        self.y = piper.recv()
        self.started = False
        self.available = None

        self.moveRandomly()

    def availableMoves(self):

        if self.terrain[self.x - 1][self.y].passable:         #Gornja pozicija
            self.available[0] = True
        if self.terrain[self.x][self.y - 1].passable:         #Leva pozicija
            self.available[1] = True
        if self.terrain[self.x][self.y + 1].passable:         #Desna pozicija
            self.available[2] = True
        if self.terrain[self.x + 1][self.y].passable:         #Donja pozicija
            self.available[3] = True

    def moveRandomly(self):

        while not self.started:                                     #Ubaciti logiku za pocetak runde
            time.sleep(3)
            break
        while True:
            task = self.piper.recv()
            #print(task)
            if task == 0:
                break
            else:
                if task == 2:
                    None                            #Ubaciti logiku za trap
                else:
                    decided = False
                    position = None
                    self.available = [False, False, False, False]
                    self.availableMoves()
                    while not decided:
                        position = random.randint(0, 3)
                        if self.available[position]:
                            decided = True

                    if position == 0:
                        self.x -= 1
                    else:
                        if position == 1:
                            self.y -= 1
                        else:
                            if position == 2:
                                self.y += 1
                            else:
                                if position == 3:
                                    self.x += 1

            sendtuple = (self.x, self.y)
            self.pipes.send(sendtuple)

            time.sleep(0.5)

            """
        self.lock = parent.NPCLock
        self.moveThread = threading.Thread(target=self.moveRandomly, args=())
        self.moveThread.start()
        
        self.lock.acquire()
            print(str(self.x) + " - " + str(self.y))
            self.lock.release()
            self.setGeometry((self.y * 40) + 16, (self.x * 40) + 16, 30, 30)
        """
