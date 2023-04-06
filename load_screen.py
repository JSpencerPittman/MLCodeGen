from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QHBoxLayout
)

from PyQt5.QtGui import QPixmap, QIcon

from PyQt5 import QtCore

import sys, os

class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()

        self.init_icon()

        self.main_layout = QHBoxLayout()

        pixmap = QPixmap('rsc/icon.png')
        self.img = QLabel()
        self.img.setPixmap(pixmap)
        self.img.setScaledContents(True)
        self.img.setMaximumSize(546,457)

        self.main_layout.addWidget(self.img)
    
        self.setLayout(self.main_layout)
        self.setWindowTitle("Loading Screen")
        self.setProperty('class', 'PRIMARY_DARK')
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(575,575)
        
        with open("style.css", 'r') as f:
            self.setStyleSheet(f.read())

    def init_icon(self):
        path = os.getcwd() + '/rsc/icon256x256.png'
        self.setWindowIcon(QIcon(path))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoadingScreen()

    with open("style.css", 'r') as f:
        app.setStyleSheet(f.read())
    
    window.show()

    app.exec()