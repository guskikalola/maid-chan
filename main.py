from PyQt5.QtWidgets import QFrame, QApplication, QPushButton, QLabel, QDesktopWidget
from PyQt5 import QtCore
from PyQt5.Qt import QPixmap, QGuiApplication
import sys
import os
import json
from time import sleep
from threading import Thread

# Maid Chan configuration
displayScreen = 1  # The screen to use

# Define the QApplication
app = QApplication([])

# Define a Desktop Widget for later values
screens = QGuiApplication.screens()
desktop = screens[displayScreen]
print(desktop.name())
screenHeight = desktop.availableGeometry().height()
screenWidth = desktop.availableGeometry().width()

# Images setup
def sortFrames(file):
    return int(file[5:len(file.replace(".png", ""))])

frames = {}
frames['maidChan'] = {}
for path, dirname, files in os.walk('./resources/img/maidChan/final/'):
    for file in sorted(files, key=sortFrames):
        frames['maidChan'][file] = QPixmap(path + file)


class maidChan(QFrame):
    def __init__(self):
        super(maidChan, self).__init__()
        # Configure the size and position of the frame
        self.resize(int(screenWidth/4), screenHeight)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("color: green")
        # Positionate the frame at the right side
        self.frameHeight = self.height()
        self.frameWidth = self.width()
        self.move(QtCore.QPoint(screenWidth - self.frameWidth,
                                screenHeight - self.frameHeight))
        # Create a QLabel to display images on it
        self.label = QLabel(parent=self)
        self.labelHeight = self.label.height()
        self.labelWidth = self.label.width()
        self.label.move(QtCore.QPoint(0, self.frameHeight - self.labelHeight))
        self.label.setPixmap(frames['maidChan']['frame2.png'])

# Execute the application
maid = maidChan()
maid.show()
app.exec_()
