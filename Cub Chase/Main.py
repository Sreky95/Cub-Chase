import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QMainWindow)


<<<<<<< Updated upstream
class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cub Chase")
=======
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
            if parent.NPC1.stunned:
                pipe1s.send(2)
            else:
                pipe1s.send(1)

            if parent.NPC2.stunned:
                pipe3s.send(2)
            else:
                pipe3s.send(1)

            if parent.NPC3.stunned:
                pipe5s.send(2)
            else:
                pipe5s.send(1)

            if parent.NPC4.stunned:
                pipe7s.send(2)
            else:
                pipe7s.send(1)

        temp1 = pipe2r.recv()
        temp2 = pipe4r.recv()
        temp3 = pipe6r.recv()
        temp4 = pipe8r.recv()
        if temp1:
            parent.NPC1.x = temp1[0]
            parent.NPC1.y = temp1[1]
            #print("1: " + str(temp1[1]) + " - " + str(temp1[0]))
            if 0 < parent.layout.TerrainMatrix[temp1[0]][temp1[1]].trap < 10:
                parent.layout.TerrainMatrix[temp1[0]][temp1[1]].trap = 0
                parent.NPC1.stunned = True
                parent.NPC1stun.emit()
        if temp2:
            parent.NPC2.x = temp2[0]
            parent.NPC2.y = temp2[1]
            #print("2: " + str(temp2[1]) + " - " + str(temp2[0]))
            if 0 < parent.layout.TerrainMatrix[temp2[0]][temp2[1]].trap < 10:
                parent.layout.TerrainMatrix[temp2[0]][temp2[1]].trap = 0
                parent.NPC2.stunned = True
                parent.NPC2stun.emit()
        if temp3:
            parent.NPC3.x = temp3[0]
            parent.NPC3.y = temp3[1]
            #print("3: " + str(temp3[1]) + " - " + str(temp3[0]))
            if 0 < parent.layout.TerrainMatrix[temp3[0]][temp3[1]].trap < 10:
                parent.layout.TerrainMatrix[temp3[0]][temp3[1]].trap = 0
                parent.NPC3.stunned = True
                parent.NPC3stun.emit()
        if temp4:
            parent.NPC4.x = temp4[0]
            parent.NPC4.y = temp4[1]
            #print("4: " + str(temp4[1]) + " - " + str(temp4[0]))
            if 0 < parent.layout.TerrainMatrix[temp4[0]][temp4[1]].trap < 10:
                parent.layout.TerrainMatrix[temp4[0]][temp4[1]].trap = 0
                parent.NPC4.stunned = True
                parent.NPC4stun.emit()

        parent.display_update.emit()
>>>>>>> Stashed changes


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title = "Cub Chase"
        self.top = 600
        self.left = 400
        self.width = 680
        self.height = 300

        self.playButton = QPushButton("PLAY", self)
        self.playButton.move(300, 125)
        self.playButton.clicked.connect(self.gameWindow)

        self.main_window()

    def main_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def gameWindow(self):
        self.mainGameWindow = GameWindow()
        self.mainGameWindow.show()
        self.hide()


<<<<<<< Updated upstream
=======
class GameWindow(QWidget):

    display_update = pyqtSignal()
    player1up = pyqtSignal()
    player1left = pyqtSignal()
    player1right = pyqtSignal()
    player1down = pyqtSignal()
    player2up = pyqtSignal()
    player2left = pyqtSignal()
    player2right = pyqtSignal()
    player2down = pyqtSignal()
    NPC1stun = pyqtSignal()
    NPC2stun = pyqtSignal()
    NPC3stun = pyqtSignal()
    NPC4stun = pyqtSignal()

    def __init__(self, parent):

        super().__init__()
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
        self.signalsconnect()

        self.mappingThread = threading.Thread(target=mapping, args=(self,))
        self.mappingThread.start()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.countdown)
        self.timer.start(3000)

    def countdown(self):

        print("Pocetak")

    def signalsconnect(self):

        self.display_update.connect(self.guiUpdate)
        self.player1up.connect(self.player1.moveup)
        self.player1left.connect(self.player1.moveleft)
        self.player1right.connect(self.player1.moveright)
        self.player1down.connect(self.player1.movedown)
        self.player2up.connect(self.player2.moveup)
        self.player2left.connect(self.player2.moveleft)
        self.player2right.connect(self.player2.moveright)
        self.player2down.connect(self.player2.movedown)
        self.NPC1stun.connect(self.NPC1.stun)
        self.NPC2stun.connect(self.NPC2.stun)
        self.NPC3stun.connect(self.NPC3.stun)
        self.NPC4stun.connect(self.NPC4.stun)

    def guiUpdate(self):

        self.NPC1.setGeometry((self.NPC1.y * 40) + 16, (self.NPC1.x * 40) + 16, 30, 30)
        self.NPC2.setGeometry((self.NPC2.y * 40) + 16, (self.NPC2.x * 40) + 16, 30, 30)
        self.NPC3.setGeometry((self.NPC3.y * 40) + 16, (self.NPC3.x * 40) + 16, 30, 30)
        self.NPC4.setGeometry((self.NPC4.y * 40) + 16, (self.NPC4.x * 40) + 16, 30, 30)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):

        key = event.key()
        player1key = False

        if key == Qt.Key_Up:
            self.player1up.emit()
            player1key = True
        else:
            if key == Qt.Key_Left:
                self.player1left.emit()
                player1key = True
            else:
                if key == Qt.Key_Right:
                    self.player1right.emit()
                    player1key = True
                else:
                    if key == Qt.Key_Down:
                        self.player1down.emit()
                        player1key = True

        if not player1key:
            if key == Qt.Key_W:
                self.player2up.emit()
            else:
                if key == Qt.Key_A:
                    self.player2left.emit()
                else:
                    if key == Qt.Key_D:
                        self.player2right.emit()
                    else:
                        if key == Qt.Key_S:
                            self.player2down.emit()

    def closeEvent(self, event):

        self.parent.show()
        self.ending = True
        self.close()


>>>>>>> Stashed changes
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
