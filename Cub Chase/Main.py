import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QMainWindow)


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cub Chase")


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
