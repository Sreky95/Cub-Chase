from PyQt5.QtWidgets import (QMainWindow, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QGridLayout,
                             QVBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap, QKeyEvent
import sys, random, math, Terrain, NPC, threading, Player, multiprocessing, time


def mapping(parent):

    pipe1s, pipe1r = multiprocessing.Pipe()
    pipe2s, pipe2r = multiprocessing.Pipe()
    pipe3s, pipe3r = multiprocessing.Pipe()
    pipe4s, pipe4r = multiprocessing.Pipe()
    pipe5s, pipe5r = multiprocessing.Pipe()
    pipe6s, pipe6r = multiprocessing.Pipe()
    pipe7s, pipe7r = multiprocessing.Pipe()
    pipe8s, pipe8r = multiprocessing.Pipe()

    npc1process = multiprocessing.Process(target=NPC.NPCMovement, args=(pipe1r,))
    pipe1s.send(pipe2s)
    pipe1s.send(parent.layout.TerrainMatrix)
    pipe1s.send(parent.NPC1.x)
    pipe1s.send(parent.NPC1.y)
    npc2process = multiprocessing.Process(target=NPC.NPCMovement, args=(pipe3r,))
    pipe3s.send(pipe4s)
    pipe3s.send(parent.layout.TerrainMatrix)
    pipe3s.send(parent.NPC2.x)
    pipe3s.send(parent.NPC2.y)
    npc3process = multiprocessing.Process(target=NPC.NPCMovement, args=(pipe5r,))
    pipe5s.send(pipe6s)
    pipe5s.send(parent.layout.TerrainMatrix)
    pipe5s.send(parent.NPC3.x)
    pipe5s.send(parent.NPC3.y)
    npc4process = multiprocessing.Process(target=NPC.NPCMovement, args=(pipe7r,))
    pipe7s.send(pipe8s)
    pipe7s.send(parent.layout.TerrainMatrix)
    pipe7s.send(parent.NPC4.x)
    pipe7s.send(parent.NPC4.y)

    npc1process.start()
    npc2process.start()
    npc3process.start()
    npc4process.start()

    while True:
        if parent.ending:
            pipe1s.send(0)
            pipe3s.send(0)
            pipe5s.send(0)
            pipe7s.send(0)
            break
        else:
            #if LOGIKA ZA TRAP:
            pipe1s.send(1)
            pipe3s.send(1)
            pipe5s.send(1)
            pipe7s.send(1)
            #else AKO JE UGAZIO U AKTIVIRAN TRAP:

        temp1 = pipe2r.recv()
        temp2 = pipe4r.recv()
        temp3 = pipe6r.recv()
        temp4 = pipe8r.recv()
        if temp1:
            parent.NPC1.x = temp1[0]
            parent.NPC1.y = temp1[1]
            #parent.NPC1.__update_position__(temp1)
            #parent.NPC1.setGeometry((temp1[1] * 40) + 16, (temp1[0] * 40) + 16, 30, 30)
            print("1: " + str(temp1[1]) + " - " + str(temp1[0]))
        if temp2:
            parent.NPC2.x = temp2[0]
            parent.NPC2.y = temp2[1]
            #parent.NPC2.__update_position__(temp2)
            #parent.NPC2.setGeometry((temp2[1] * 40) + 16, (temp2[0] * 40) + 16, 30, 30)
            print("2: " + str(temp2[1]) + " - " + str(temp2[0]))
        if temp3:
            parent.NPC3.x = temp3[0]
            parent.NPC3.y = temp3[1]
            #parent.NPC3.__update_position__(temp3)
            #parent.NPC3.setGeometry((temp3[1] * 40) + 16, (temp3[0] * 40) + 16, 30, 30)
            print("3: " + str(temp3[1]) + " - " + str(temp3[0]))
        if temp4:
            parent.NPC4.x = temp4[0]
            parent.NPC4.y = temp4[1]
            #parent.NPC4.__update_position__(temp4)
            #parent.NPC4.setGeometry((temp4[1] * 40) + 16, (temp4[0] * 40) + 16, 30, 30)
            print("4: " + str(temp4[1]) + " - " + str(temp4[0]))

        parent.display_update.emit()


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.title = "Cub Chase"
        self.top = 400
        self.left = 600
        self.width = 680
        self.height = 300
        self.mainGameWindow = None

        self.playButton = QPushButton("PLAY", self)
        self.playButton.move(300, 125)
        self.playButton.clicked.connect(self.gameWindow)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def gameWindow(self):

        self.mainGameWindow = GameWindow(self)
        self.mainGameWindow.show()
        self.hide()


class GameWindow(QWidget):

    display_update = pyqtSignal()

    def __init__(self, parent):

        super().__init__()
        self.display_update.connect(self.guiUpdate)
        self.setWindowTitle("Cub Chase")
        self.parent = parent
        self.freespaces = 0
        self.ending = False
        self.NPC1 = None
        self.NPC2 = None
        self.NPC3 = None
        self.NPC4 = None
        self.layout = Terrain.GameTerrain(self, 15)
        self.NPC1 = NPC.NPC(self)
        self.NPC2 = NPC.NPC(self)
        self.NPC3 = NPC.NPC(self)
        self.NPC4 = NPC.NPC(self)
        self.player1 = Player.Player(self, 1)
        self.player2 = Player.Player(self, 2)

        self.mappingThread = threading.Thread(target=mapping, args=(self,))
        self.mappingThread.start()

    def guiUpdate(self):

        self.NPC1.setGeometry((self.NPC1.y * 40) + 16, (self.NPC1.x * 40) + 16, 30, 30)
        self.NPC2.setGeometry((self.NPC2.y * 40) + 16, (self.NPC2.x * 40) + 16, 30, 30)
        self.NPC3.setGeometry((self.NPC3.y * 40) + 16, (self.NPC3.x * 40) + 16, 30, 30)
        self.NPC4.setGeometry((self.NPC4.y * 40) + 16, (self.NPC4.x * 40) + 16, 30, 30)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):

        key = event.key()
        player1key = False
        player2key = False

        if key == Qt.Key_Up:
            #self.player1.x -= 1
            player1key = True
        else:
            if key == Qt.Key_Left:
                #self.player1.y -= 1
                player1key = True
            else:
                if key == Qt.Key_Right:
                    #self.player1.y += 1
                    player1key = True
                else:
                    if key == Qt.Key_Down:
                        #self.player1.x += 1
                        player1key = True

        if not player1key:
            if key == Qt.Key_W:
                #self.player2.x -= 1
                player2key = True
            else:
                if key == Qt.Key_A:
                    #self.player2.y -= 1
                    player2key = True
                else:
                    if key == Qt.Key_D:
                        #self.player2.y += 1
                        player2key = True
                    else:
                        if key == Qt.Key_S:
                            #self.player2.x += 1
                            player2key = True


        if player1key:              #zameniti sa logikom za proveravanje kretanja itd, sa Qsignalom pokrenuti funkciju
            self.player1.setGeometry((self.player1.y * 40) + 16, (self.player1.x * 40) + 16, 30, 30)
        else:
            if player2key:
                self.player2.setGeometry((self.player2.y * 40) + 16, (self.player2.x * 40) + 16, 30, 30)

    def closeEvent(self, event):

        self.parent.show()
        self.ending = True
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
