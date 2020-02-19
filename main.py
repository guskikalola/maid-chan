from PyQt5.QtWidgets import QFrame, QApplication, QPushButton, QLabel
from PyQt5 import QtCore
from PyQt5.Qt import QPixmap, QGuiApplication, QObject, QThread, QMetaObject, Q_ARG, pyqtSlot
import sys
import os
import json
from time import sleep
from threading import Thread, main_thread

# Maid Chan configuration
displayScreen = 1  # The screen to use

# Define the QApplication
app = QApplication([])

# Define a Desktop Widget for later values
screens = QGuiApplication.screens()
desktop = screens[displayScreen]
mainObject = QObject()
screenHeight = desktop.availableGeometry().height()
screenWidth = desktop.availableGeometry().width()

# Images setup


def sortFrames(file):
    return int(file[5:len(file.replace(".PNG", ""))])



class maidChan(QFrame):
    def __init__(self):
        super(maidChan, self).__init__()
        # Define some class necesary parameters
        self.thread = False
        # Lower means faster ( animationSpeed = Sleep between frames )
        self.animationSpeed = 0.07
        # Configure the size and position of the frame
        self.resize(int(screenWidth/4), screenHeight)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setFrameShape(QFrame.Box)
        self.setStyleSheet("color: green")
        # Positionate the frame at the right side
        self.frameHeight = self.height()
        self.frameWidth = self.width()
        self.move(QtCore.QPoint(screenWidth - self.frameWidth,
                                screenHeight - self.frameHeight))
        # Create a QLabel to display images on it
        self.label = QLabel(parent=self)
        self.label.setAlignment(QtCore.Qt.AlignBottom)
        self.label.setScaledContents(True)
        self.labelHeight = self.label.height()
        self.labelWidth = self.label.width()
        # Create Qlabel for notifications
        self.notificationBox = QLabel(parent=self)
        self.notificationContent = QLabel(parent=self.notificationBox)
    @pyqtSlot(str)
    def notificate(self, notification):
        # Create a QLabel to display notification on it
        self.notificationBox.setAlignment(QtCore.Qt.AlignLeft)
        self.notificationContent.setAlignment(QtCore.Qt.AlignJustify)
        self.notificationBox.setScaledContents(True)
        self.notificationBoxHeight = self.notificationBox.height()
        self.notificationBoxWidth = self.notificationBox.width()
        self.notificationBox.setPixmap(
            QPixmap('./resources/img/notification/frame0.PNG'))
        self.notificationBox.adjustSize()
        self.notificationBox.move(QtCore.QPoint(0, 300))
        notificationBoxHeight = self.notificationBox.geometry().height()
        notificationBoxWidth = self.notificationBox.geometry().width()
        self.notificationContent.setWordWrap(True)
        self.notificationContent.resize(notificationBoxWidth,notificationBoxHeight)
        self.notificationContent.setTextFormat(QtCore.Qt.RichText)
        self.notificationContent.setText(notification)
        self.notificationContent.move(QtCore.QPoint(int(notificationBoxWidth/9),int(notificationBoxWidth/4)))

    def startAnimation(self, label, path, notification):
        frames = {}
        for root, name, files in os.walk(path):
            for file in files:
                    frames[file] = QPixmap(root+"/"+file)
            for key in sorted(frames.keys(), key=sortFrames):
                pixmap = frames[key]  # List of animation frames (Pixmaps)
                pixmapWidth = pixmap.size().width()
                pixmapHeight = pixmap.size().height()
                label.resize(pixmapWidth, pixmapHeight)
                label.move(QtCore.QPoint(
                    0, self.frameHeight - pixmapHeight))
                label.setPixmap(pixmap)
                sleep(self.animationSpeed)
            QMetaObject.invokeMethod(
                self, "notificate", QtCore.Qt.QueuedConnection, Q_ARG(str, notification)
            )

    def createNotification(self, notification):
        # Create a new thread
        if self.thread:  # If there is already a thread running, wait for it.
            self.thread.join()  # Wait for the thread to end it's task.
            self.thread = Thread(target=self.startAnimation, args=(
                self.label, './resources/img/maidChan/newNotification', notification,))
        else:
            self.thread = Thread(target=self.startAnimation, args=(
                self.label, './resources/img/maidChan/newNotification', notification,))

        # Show the frame if it's hidden
        if self.isHidden() == True:
            self.show()

        self.thread.start()  # Proced to run the startAnimation function

# Execute the application
maid = maidChan()
maid.createNotification("<h1> Aiuda tengo miedo.<br/><h5>Vivan las lolis</h5>")
app.exec_()
app.exit()
