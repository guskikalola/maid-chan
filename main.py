#############################################
#                                           #
#                Maid-chan's                # 
#           Notification System             # 
#             by guskikalola                #
#                                           #
#############################################

# Load application config from the config.json
from time import sleep
import json
import os
with open('./config.json') as configFile_data:
    configFile = json.load(configFile_data)
# Define the main application where everything will run
from PyQt5.QtWidgets import QApplication,QFrame, QDesktopWidget, QLabel
from PyQt5.Qt import QThread,Qt, QPoint, QMovie,QPixmap, QTextDocument
app = QApplication([])
# Setup screen configuration
config_selectedScreen = configFile["SelectedScreen"]
screens = app.screens()
selectedScreen = screens[config_selectedScreen]

# Thread where maidchan works
class maid(QThread):
    def consumeNotification(self):
        notification = self.notificationQueue.pop(0)
        return json.loads(str(notification).replace("\'","\""))
    def createNotification(self):
        
        animationSpeed = 0.09
        notificationLifeTime = 6
        imgSize = 218
        
        self.working = True
        content = self.consumeNotification()
        if(content == "False"): 
            self.working = False
            return False
        frames = {}
        def sortFrames(file):
            return int(file[5:len(file.replace(".PNG", ""))])
        for root, name, files in os.walk('./resources/img/maidChan/notification/'):
            for file in files:
                frames[file] = QPixmap(root+"/"+file)
            for key in sorted(frames.keys(), key=sortFrames):
                pixmap = frames[key]  # List of animation frames (Pixmaps)
                pixmap = pixmap.scaled(imgSize, imgSize, Qt.KeepAspectRatio)
                pixmapWidth = pixmap.size().width()
                pixmapHeight = pixmap.size().height()
                self.animationLabel.resize(pixmapWidth, pixmapHeight)
                self.animationLabel.move(QPoint(
                    0, self.window.height() - pixmapHeight))
                self.animationLabel.setPixmap(pixmap)
                self.animationLabel.show()
                sleep(animationSpeed)
        frames = {}
        self.notificationLabel.show()
        self.notificationImage.show()
        self.notificationLabel.show()
        self.notificationLabel.setText(
            "Ha recibido un correo de: \n" + content["from"] + "\nAsunto:\n" + content["subject"] + "\n❤️")
        sleep(notificationLifeTime)
        self.working = False
        self.animationLabel.hide()
        self.notificationImage.hide()
        self.notificationLabel.hide()
    def __init__(self):
        super(maid, self).__init__()
        self.working = False

    # Configure the application frame
        self.window = QFrame()
        self.window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.window.setWindowFlag(Qt.FramelessWindowHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)
        # Debugging
        if(configFile["debug"] == True):
            self.window.setFrameShape(QFrame.Box)
            self.window.setStyleSheet("color: green")
        self.window.show()
        # Move the frame to the selected screen
        windowPosition = QPoint(selectedScreen.availableGeometry().right() - self.window.width(), 
                                selectedScreen.availableGeometry().bottom() - self.window.height())
        self.window.move(windowPosition)

        # Setup the notification stuff
        self.notificationQueue = []
        self.notificationImage = QLabel(parent=self.window)
        self.notificationImage.resize(128*4, 128*2)
        self.notificationImage.move(self.notificationImage.mapFromParent(QPoint(self.window.width(
        ) - self.notificationImage.width(), 0)))
        notificationFrame = QPixmap(
            "./resources/img/notification/frame0.PNG")
        notificationFrame = notificationFrame.scaled(
            self.notificationImage.width(), self.notificationImage.height(),Qt.IgnoreAspectRatio)
        self.notificationImage.setPixmap(notificationFrame)
        # Setup the label to display animation and the label to display notification
        self.animationLabel = QLabel("GIF",parent=self.window)
        self.animationLabel.resize(128*2, 128*2)
        self.animationLabel.move(self.animationLabel.mapFromParent(QPoint(0, self.window.height() - self.animationLabel.height())))

        self.notificationLabel = QLabel(parent=self.notificationImage)
        self.notificationLabel.setAlignment(Qt.AlignCenter)
        self.notificationLabel.setStyleSheet("color: black; font-size:18px")
        self.notificationLabel.resize(128*4, 128*2)
        self.notificationLabel.move(self.notificationLabel.mapFromParent(QPoint(0,0)))


        if(configFile["debug"] == True):
            self.animationLabel.setFrameShape(QFrame.Box)
            self.animationLabel.setStyleSheet("color: red")

            self.notificationLabel.setFrameShape(QFrame.Box)
            self.notificationLabel.setStyleSheet("color: red")
            
            self.notificationImage.setFrameShape(QFrame.Box)
            self.notificationImage.setStyleSheet("color: yellow")

        # self.notificationImage.show()
        # self.notificationLabel.show()

        print("Window created at " + self.window.screen().name() + "!")


# Init the maid's duties
maidchan = maid()

# [MODULES]
modules = configFile["modules"]
if(modules["email"]):
    from modules.maid_mail import listener
    # Listen for new emails and notificate
    listener.login() # Login to the supplied account
    listener.read() # Initial email read ( To load the basic structure )
    listener.start(maidchan) # Start the listener ( argument is used for callbacks )


# Exit the application
app.exec_() # Run the app
app.closeAllWindows() # When the app stops running close every app's window
app.exit() # Exit the app
