from PyQt5.QtWidgets import (QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QGridLayout,
                             QVBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap
import sys, random, math


class GameTerrain(QGridLayout):

    def __init__(self, parent, size):
        super().__init__(parent)
        self.parentGameWindow = parent
        self.terrainwidth = size
        self.terrainheight = size
        parent.setGeometry(550, 100, 40, 40)
        self.setSpacing(0)
        self.Trap1spawned = False
        loaded = False

        while not loaded:

            self.parentGameWindow.freespaces = 0
            self.TerrainMatrix = [[0 for x in range(self.terrainwidth)] for y in range(self.terrainheight)]
            middle1 = self.terrainwidth / 2
            middle2 = self.terrainheight / 2

            for y in range(len(self.TerrainMatrix)):
                for x in range(len(self.TerrainMatrix[y])):
                    if (x == math.floor(middle1) and y == math.floor(middle2) or
                    x == math.floor(middle1) - 1 and y == math.floor(middle2) or
                    x == math.floor(middle1) + 1 and y == math.floor(middle2) or
                    x == math.floor(middle1) and y == math.floor(middle2) - 1 or
                    x == math.floor(middle1) and y == math.floor(middle2) + 1):
                        self.TerrainMatrix[x][y] = TerrainTile(2, True)
                    else:
                        if (x == math.floor(middle1) - 2 and y == math.floor(middle2) - 2 or
                        x == math.floor(middle1) - 2 and y == math.floor(middle2) + 2 or
                        x == math.floor(middle1) + 2 and y == math.floor(middle2) - 2 or
                        x == math.floor(middle1) + 2 and y == math.floor(middle2) + 2):
                            self.TerrainMatrix[x][y] = TerrainTile(2, False)
                        else:
                            if (x == 0 or x == self.terrainwidth - 1 or y == 0 or y == self.terrainheight - 1 or
                            x == math.floor(middle1) + 1 and y == math.floor(middle2) + 1 or
                            x == math.floor(middle1) + 1 and y == math.floor(middle2) - 1 or
                            x == math.floor(middle1) - 1 and y == math.floor(middle2) + 1 or
                            x == math.floor(middle1) - 1 and y == math.floor(middle2) - 1):
                                self.TerrainMatrix[x][y] = TerrainTile(0, True)
                            else:
                                if (x == math.floor(middle1) - 2 and
                                                    y == math.floor(middle2) - 1 or
                                    x == math.floor(middle1) - 2 and
                                                    y == math.floor(middle2) or
                                    x == math.floor(middle1) - 2 and
                                                    y == math.floor(middle2) + 1 or
                                    x == math.floor(middle1) + 2 and
                                                    y == math.floor(middle2) - 1 or
                                    x == math.floor(middle1) + 2 and
                                                    y == math.floor(middle2) or
                                    x == math.floor(middle1) + 2 and
                                                    y == math.floor(middle2) + 1 or
                                    x == math.floor(middle1) - 1 and
                                                    y == math.floor(middle2) - 2 or
                                    x == math.floor(middle1) and
                                                    y == math.floor(middle2) - 2 or
                                    x == math.floor(middle1) + 1 and
                                                    y == math.floor(middle2) - 2 or
                                    x == math.floor(middle1) - 1 and
                                                    y == math.floor(middle2) + 2 or
                                    x == math.floor(middle1) and
                                                    y == math.floor(middle2) + 2 or
                                    x == math.floor(middle1) + 1 and
                                                    y == math.floor(middle2) + 2):
                                    self.TerrainMatrix[x][y] = TerrainTile(1, False)
                                else:
                                    if x == math.floor(middle1) and y > math.floor(middle2):
                                        self.TerrainMatrix[x][y] = TerrainTile(1, False)
                                    else:
                                        self.TerrainMatrix[x][y] = TerrainTile(random.randint(0, 2), False)

            for y in range(len(self.TerrainMatrix)):
                for x in range(len(self.TerrainMatrix[y])):
                    if y > 0 and x > 0:
                        if not self.checkIfReachable(x, y):
                            self.TerrainMatrix[x][y].terraintype = 0
                            self.TerrainMatrix[x][y].passable = False
                        for j in range(len(self.TerrainMatrix)):
                            for i in range(len(self.TerrainMatrix[j])):
                                self.TerrainMatrix[i][j].terraintype = abs(self.TerrainMatrix[i][j].terraintype)

            while not self.Trap1spawned:
                x = random.randint(1, len(self.TerrainMatrix[0]) - 1)
                y = random.randint(1, len(self.TerrainMatrix) - 1)
                if self.TerrainMatrix[x][y].passable and not self.TerrainMatrix[x][y].trap:
                    self.TerrainMatrix[x][y].trap = 10
                    self.Trap1spawned = True

            for n in range(len(self.TerrainMatrix)):
                for k in range(len(self.TerrainMatrix[n])):
                    if self.TerrainMatrix[k][n].passable:
                        self.parentGameWindow.freespaces += 1

            if self.parentGameWindow.freespaces > 20:                                                #Moze da se podesi granica
                loaded = True

        self.paintTerrain()

    def paintTerrain(self):
        for y in range(len(self.TerrainMatrix)):
            for x in range(len(self.TerrainMatrix[y])):
                tempterrain = self.TerrainMatrix[x][y].terraintype
                if (tempterrain == 0):
                    self.paintWall(x, y)
                else:
                    if (tempterrain == 1):
                        if self.TerrainMatrix[x][y].trap == 10:
                            templabel = QLabel()
                            temppicture = QPixmap("./Pictures/SandTrapInactive.png")
                            templabel.setPixmap(temppicture.scaled(40, 40))
                            self.addWidget(templabel, x, y)
                        else:
                            templabel = QLabel()
                            temppicture = QPixmap("./Pictures/Sand.png")
                            templabel.setPixmap(temppicture.scaled(40, 40))
                            self.addWidget(templabel, x, y)
                    else:
                        if (tempterrain == 2):
                            if self.TerrainMatrix[x][y].trap == 10:
                                templabel = QLabel()
                                temppicture = QPixmap("./Pictures/GrassTrapInactive.png")
                                templabel.setPixmap(temppicture.scaled(40, 40))
                                self.addWidget(templabel, x, y)
                            else:
                                templabel = QLabel()
                                temppicture = QPixmap("./Pictures/Grass.png")
                                templabel.setPixmap(temppicture.scaled(40, 40))
                                self.addWidget(templabel, x, y)

    def paintWall(self, x, y):
        templabel = QLabel()
        neighbours = [0, 0, 0, 0, 0, 0, 0, 0]
        neighbours = self.checkForNeighbouringWalls(x, y, neighbours)
        if neighbours[1] == 1 and neighbours[3] == 0 and neighbours[4] == 0 and neighbours[6] == 1:
            temppicture = QPixmap("./Pictures/2LR.png")
        if neighbours[1] == 0 and neighbours[3] == 1 and neighbours[4] == 1 and neighbours[6] == 0:
            temppicture = QPixmap("./Pictures/2UD.png")
        if (neighbours[1] == 1 and neighbours[3] == 1 and neighbours[4] == 1 and neighbours[6] == 1 and
        neighbours[0] == 1 and neighbours[2] == 1 and neighbours[5] == 1 and neighbours[7] == 1):
            temppicture = QPixmap("./Pictures/8All.png")
        if neighbours[1] == 1 and neighbours[3] == 1 and neighbours[4] == 0 and neighbours[6] == 0:
            if neighbours[0] == 1:
                temppicture = QPixmap("./Pictures/3UL.png")
            else:
                temppicture = QPixmap("./Pictures/2UL.png")
        if neighbours[1] == 0 and neighbours[3] == 1 and neighbours[4] == 0 and neighbours[6] == 1:
            if neighbours[5] == 1:
                temppicture = QPixmap("./Pictures/3UR.png")
            else:
                temppicture = QPixmap("./Pictures/2UR.png")
        if neighbours[1] == 1 and neighbours[3] == 0 and neighbours[4] == 1 and neighbours[6] == 0:
            if neighbours[2] == 1:
                temppicture = QPixmap("./Pictures/3LD.png")
            else:
                temppicture = QPixmap("./Pictures/2LD.png")
        if neighbours[1] == 0 and neighbours[3] == 0 and neighbours[4] == 1 and neighbours[6] == 1:
            if neighbours[7] == 1:
                temppicture = QPixmap("./Pictures/3RD.png")
            else:
                temppicture = QPixmap("./Pictures/2RD.png")

        if neighbours[1] == 0 and neighbours[3] == 0 and neighbours[4] == 0 and neighbours[6] == 0:
            temppicture = QPixmap("./Pictures/Center.png")
        if neighbours[1] == 1 and neighbours[3] == 0 and neighbours[4] == 0 and neighbours[6] == 0:
            temppicture = QPixmap("./Pictures/1L.png")
        if neighbours[1] == 0 and neighbours[3] == 1 and neighbours[4] == 0 and neighbours[6] == 0:
            temppicture = QPixmap("./Pictures/1U.png")
        if neighbours[1] == 0 and neighbours[3] == 0 and neighbours[4] == 1 and neighbours[6] == 0:
            temppicture = QPixmap("./Pictures/1D.png")
        if neighbours[1] == 0 and neighbours[3] == 0 and neighbours[4] == 0 and neighbours[6] == 1:
            temppicture = QPixmap("./Pictures/1R.png")

        if (neighbours[0] == 1 and neighbours[1] == 1 and neighbours[2] == 1 and neighbours[6] == 0 and
            neighbours[3] == 1 and neighbours[4] == 1):
            temppicture = QPixmap("./Pictures/3L.png")
        if (neighbours[0] == 1 and neighbours[3] == 1 and neighbours[5] == 1 and neighbours[4] == 0 and
            neighbours[1] == 1 and neighbours[6] == 1):
            temppicture = QPixmap("./Pictures/3U.png")
        if (neighbours[5] == 1 and neighbours[6] == 1 and neighbours[7] == 1 and neighbours[1] == 0 and
            neighbours[3] == 1 and neighbours[4] == 1):
            temppicture = QPixmap("./Pictures/3R.png")
        if (neighbours[2] == 1 and neighbours[4] == 1 and neighbours[7] == 1 and neighbours[3] == 0 and
            neighbours[1] == 1 and neighbours[6] == 1):
            temppicture = QPixmap("./Pictures/3D.png")

        if neighbours[1] == 1 and neighbours[4] == 1 and neighbours[6] == 1:
            if neighbours[3] == 0 and neighbours[2] == 0 and neighbours[7] == 0:
                temppicture = QPixmap("./Pictures/3LDR.png")
            else:
                if neighbours[0] == 1 and neighbours[3] == 1 and neighbours[5] == 1 and neighbours[2] == 0 and \
                        neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/5LDR.png")
                else:
                    if neighbours[3] == 0 and neighbours[2] == 1 and neighbours[7] == 0:
                        temppicture = QPixmap("./Pictures/4LD2.png")
                    if neighbours[3] == 0 and neighbours[2] == 0 and neighbours[7] == 1:
                        temppicture = QPixmap("./Pictures/4RD.png")
        if neighbours[1] == 1 and neighbours[3] == 1 and neighbours[4] == 1:
            if neighbours[6] == 0 and neighbours[0] == 0 and neighbours[2] == 0:
                temppicture = QPixmap("./Pictures/3ULD.png")
            else:
                if neighbours[5] == 1 and neighbours[6] == 1 and neighbours[7] == 1 and neighbours[0] == 0 and \
                        neighbours[2] == 0:
                    temppicture = QPixmap("./Pictures/5ULD.png")
                else:
                    if neighbours[6] == 0 and neighbours[0] == 1 and neighbours[2] == 0:
                        temppicture = QPixmap("./Pictures/4UL2.png")
                    if neighbours[6] == 0 and neighbours[0] == 0 and neighbours[2] == 1:
                        temppicture = QPixmap("./Pictures/4LD.png")
        if neighbours[1] == 1 and neighbours[3] == 1 and neighbours[6] == 1:
            if neighbours[4] == 0 and neighbours[0] == 0 and neighbours[5] == 0:
                temppicture = QPixmap("./Pictures/3ULR.png")
            else:
                if neighbours[2] == 1 and neighbours[4] == 1 and neighbours[7] == 1 and neighbours[0] == 0 and \
                        neighbours[5] == 0:
                    temppicture = QPixmap("./Pictures/5ULR.png")
                else:
                    if neighbours[4] == 0 and neighbours[0] == 1 and neighbours[5] == 0:
                        temppicture = QPixmap("./Pictures/4UL.png")
                    if neighbours[4] == 0 and neighbours[0] == 0 and neighbours[5] == 1:
                        temppicture = QPixmap("./Pictures/4UR2.png")
        if neighbours[3] == 1 and neighbours[4] == 1 and neighbours[6] == 1:
            if neighbours[1] == 0 and neighbours[5] == 0 and neighbours[7] == 0:
                temppicture = QPixmap("./Pictures/3URD.png")
            else:
                if neighbours[0] == 1 and neighbours[1] == 1 and neighbours[2] == 1 and neighbours[5] == 0 and \
                        neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/5URD.png")
                else:
                    if neighbours[1] == 0 and neighbours[5] == 1 and neighbours[7] == 0:
                        temppicture = QPixmap("./Pictures/4UR.png")
                    if neighbours[1] == 0 and neighbours[5] == 0 and neighbours[7] == 1:
                        temppicture = QPixmap("./Pictures/4RD2.png")

        if neighbours[1] == 1 and neighbours[3] == 1 and neighbours[4] == 1 and neighbours[6] == 1:
            if neighbours[0] == 0 and neighbours[2] == 0 and neighbours[5] == 0 and neighbours[7] == 0:
                temppicture = QPixmap("./Pictures/4All.png")
            else:
                if neighbours[0] == 1 and neighbours[2] == 1 and neighbours[5] == 1 and neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/7UL.png")
                if neighbours[0] == 1 and neighbours[2] == 1 and neighbours[5] == 0 and neighbours[7] == 1:
                    temppicture = QPixmap("./Pictures/7LD.png")
                if neighbours[0] == 1 and neighbours[2] == 0 and neighbours[5] == 1 and neighbours[7] == 1:
                    temppicture = QPixmap("./Pictures/7UR.png")
                if neighbours[0] == 0 and neighbours[2] == 1 and neighbours[5] == 1 and neighbours[7] == 1:
                    temppicture = QPixmap("./Pictures/7RD.png")
                if neighbours[0] == 0 and neighbours[2] == 1 and neighbours[5] == 0 and neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/5LD.png")
                if neighbours[0] == 0 and neighbours[2] == 0 and neighbours[5] == 0 and neighbours[7] == 1:
                    temppicture = QPixmap("./Pictures/5RD.png")
                if neighbours[0] == 1 and neighbours[2] == 0 and neighbours[5] == 0 and neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/5UL.png")
                if neighbours[0] == 0 and neighbours[2] == 0 and neighbours[5] == 1 and neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/5UR.png")
                if neighbours[0] == 1 and neighbours[2] == 0 and neighbours[5] == 0 and neighbours[7] == 1:
                    temppicture = QPixmap("./Pictures/6Diag.png")
                if neighbours[0] == 0 and neighbours[2] == 1 and neighbours[5] == 1 and neighbours[7] == 0:
                    temppicture = QPixmap("./Pictures/6Diag2.png")

        templabel.setPixmap(temppicture.scaled(40, 40))
        self.addWidget(templabel, x, y)

    def checkForNeighbouringWalls(self, x, y, neighbours):
        if x == 0:
            neighbours[0] = 1
            neighbours[3] = 1
            neighbours[5] = 1
        if x == self.terrainwidth - 1:
            neighbours[2] = 1
            neighbours[4] = 1
            neighbours[7] = 1
        if y == 0:
            neighbours[0] = 1
            neighbours[1] = 1
            neighbours[2] = 1
        if y == self.terrainheight - 1:
            neighbours[5] = 1
            neighbours[6] = 1
            neighbours[7] = 1
        if x != 0 and y != 0:
            if self.TerrainMatrix[x - 1][y - 1].terraintype == 0:
                neighbours[0] = 1
        if y != 0:
            if self.TerrainMatrix[x][y - 1].terraintype == 0:
                neighbours[1] = 1
        if x != self.terrainwidth - 1 and y != 0:
            if self.TerrainMatrix[x + 1][y - 1].terraintype == 0:
                neighbours[2] = 1
        if x != 0:
            if self.TerrainMatrix[x - 1][y].terraintype == 0:
                neighbours[3] = 1
        if x != self.terrainwidth - 1:
            if self.TerrainMatrix[x + 1][y].terraintype == 0:
                neighbours[4] = 1
        if x != 0 and y != self.terrainheight - 1:
            if self.TerrainMatrix[x - 1][y + 1].terraintype == 0:
                neighbours[5] = 1
        if y != self.terrainheight - 1:
            if self.TerrainMatrix[x][y + 1].terraintype == 0:
                neighbours[6] = 1
        if x != self.terrainwidth - 1 and y != self.terrainheight - 1:
            if self.TerrainMatrix[x + 1][y + 1].terraintype == 0:
                neighbours[7] = 1
        return neighbours


    def checkIfReachable(self, x, y):
        reachable = False
        if x == math.floor(len(self.TerrainMatrix) / 2) and y == math.floor(len(self.TerrainMatrix[0]) / 2):
            self.TerrainMatrix[x][y].terraintype = abs(self.TerrainMatrix[x][y].terraintype)
            return True
        else:
            if self.TerrainMatrix[x][y].terraintype == 0:
                self.TerrainMatrix[x][y].terraintype = abs(self.TerrainMatrix[x][y].terraintype)
                return False
            else:
                self.TerrainMatrix[x][y].terraintype = -self.TerrainMatrix[x][y].terraintype
                if not reachable and self.TerrainMatrix[x - 1][y].terraintype > 0:
                    reachable = self.checkIfReachable(x - 1, y)
                if not reachable and self.TerrainMatrix[x + 1][y].terraintype > 0:
                    reachable = self.checkIfReachable(x + 1, y)
                if not reachable and self.TerrainMatrix[x][y - 1].terraintype > 0:
                    reachable = self.checkIfReachable(x, y - 1)
                if not reachable and self.TerrainMatrix[x][y + 1].terraintype > 0:
                    reachable = self.checkIfReachable(x, y + 1)
                return reachable

    def replacePrints(self, position, player):

        if player == 1:
            temppicture = QPixmap("./Pictures/SandPrints1.png")
        else:
            if player == 2:
                temppicture = QPixmap("./Pictures/SandPrints2.png")

        self.itemAt(position).widget().setPixmap(temppicture.scaled(40, 40))

        for y in range(len(self.TerrainMatrix)):
            for x in range(len(self.TerrainMatrix[0])):
                temp = self.TerrainMatrix[x][y]
                if temp.terraintype == 1 and temp.footprints == 0:
                    return

        temppicture = QPixmap("./Pictures/Sand.png")
        self.itemAt(len(self.TerrainMatrix) * len(self.TerrainMatrix[0]) - len(self.TerrainMatrix) / 2)\
            .widget().setPixmap(temppicture.scaled(40, 40))
        #LOGIKA ZA KRAJ PARTIJE

    def activateTrap(self, position, player, terrain):

        print(player)
        print(terrain)
        if player == 1:
            if terrain == 1:
                temppicture = QPixmap("./Pictures/SandTrapBlue.png")
            else:
                temppicture = QPixmap("./Pictures/GrassTrapBlue.png")
        if player == 2:
            if terrain == 1:
                temppicture = QPixmap("./Pictures/SandTrapRed.png")
            else:
                temppicture = QPixmap("./Pictures/GrassTrapRed.png")
        self.itemAt(position).widget().setPixmap(temppicture.scaled(40, 40))

    def deleteTrap(self, position, terrain):

        if terrain == 1:
            temppicture = QPixmap("./Pictures/Sand.png")
        else:
            temppicture = QPixmap("./Pictures/Grass.png")
        self.itemAt(position).widget().setPixmap(temppicture.scaled(40, 40))


class TerrainTile(object):

    def __init__(self, terraintype, safezone):
        self.terraintype = terraintype
        if terraintype == 0:
            self.passable = False
        else:
            if safezone:
                self.passable = False
            else:
                self.passable = True
        self.footprints = 0
        self.trap = 0
