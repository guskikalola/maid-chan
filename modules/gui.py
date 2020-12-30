#############################################
#                                           #
#                  [MODULE]                 #
#           Graphic User Interface          #
#                                           #
#############################################
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QFrame, QHBoxLayout, QGridLayout
from PyQt5.Qt import QApplication, QObject, QIcon, QThread, QSizeGrip, QRect, QLineEdit, QListWidget, QLabel
from PyQt5.Qt import Qt
from main import Main



class GUI(QThread):
    # Init the GUI's main window
    def export(self,imported):
        self.clock, = imported 
    def __init__(self):
        super(GUI, self).__init__()
        
        # GUI Design
        self.window = QWidget()
        self.window.setWindowTitle("Maid-chan GUI")
        self.window.setWindowIcon(
            QIcon("./resources/img/maidChan/notification/Frame5.PNG"))
        self.window.setStyleSheet("background-color:#424242")
        self.window.setWindowFlag(Qt.FramelessWindowHint)

        # self.topBarContainer = QHBoxLayout()
        self.contentContainer = QGridLayout(self.window)

        self.sizegrip = QSizeGrip(self.window)

        self.topBar = QFrame(parent=self.window)
        self.topBar.setStyleSheet("background-color:#303030")
        self.topBar.show()

        self.exitButton = QFrame(parent=self.window)
        self.exitButton.setStyleSheet("background-color:#e57373")
        self.exitButton.mousePressEvent = self.close
        self.exitButton.setCursor(Qt.PointingHandCursor)
        self.exitButton.show()

        # self.topBarContainer.setContentsMargins(0,0,0,0)
        # self.topBarContainer.setSpacing(0)
        # self.topBarContainer.addWidget(self.topBar)
        # self.topBarContainer.addWidget(self.exitButtonq)

        """ 
                GUI Content
        """
        
        # Alarm TAB
        self.tab1_layout = QGridLayout()
        self.tab2_layout = QGridLayout()
        
        self.tab1 = QWidget(parent=self.window)
        self.tab1.setStyleSheet("background-color:red")
        self.tab1.setLayout(self.tab1_layout)
        
        self.alarm_input = QLineEdit()
        def addAlarm():
            time = self.alarm_input.text().split(":")
            self.alarm_input.clear()
            if(len(time) < 2):
                return False
            elif type(time[1]) is str:
                self.clock.addAlarm(hour=time[0], minute=time[1])
                load_alarms()
        self.alarm_input.editingFinished.connect(addAlarm)
        self.alarm_list = QListWidget(parent=self.window)
        def itemClicked(item):
            print(item)
        self.alarm_list.itemClicked.connect(itemClicked)
        def load_alarms():
            self.alarm_list.clear()
            alarms = self.clock.getAlarms() 
            for alarm in alarms:
                id,h,m,ts,d = alarm
                if(len(str(m)) < 2):
                    m = "0" + str(m)
                if(len(str(h)) < 2):
                    h = "0" + str(h)
                
                self.alarm_list.insertItem(0,"%s:%s" % (h,m))
        self.tab1_layout.addWidget(self.alarm_input,0,0,30,100)
        self.tab1_layout.addWidget(self.alarm_list,1,0,25,25)
        self.tab1.show()
        # ??? TAB
        # self.tab2 = QFrame(parent=self.window)
        # self.tab2.setStyleSheet("background-color:blue")
        # self.tab2.setLayout(self.tab2_layout)
        # self.tab2.show()

        # self.contentContainer.setContentsMargins(0, 30, 0, 0)
        self.contentContainer.setHorizontalSpacing(0)
        self.contentContainer.setVerticalSpacing(20)
        # self.contentContainer.setColumnStretch(0,10)
        self.contentContainer.setColumnStretch(1,10)
        self.contentContainer.addWidget(self.topBar,0,0)
        # self.contentContainer.addWidget(self.sizegrip,0,1)
        self.contentContainer.addWidget(self.exitButton,0,1)
        self.contentContainer.addWidget(self.tab1,1,0)
        # self.contentContainer.addWidget(self.tab2,1,3)
        

        # Window functionality

        # self.sizegrip = QSizeGrip(self.window)
        # self.topBarContainer.addWidget(self.sizegrip)

        self.dragging = False

        def drag(e):
            if(self.dragging == True):
                self.window.move(e.globalX() - self.offset.x() - 10,
                                 e.globalY() - self.offset.y() - 10)

        def toggleDragging(e):
            self.offset = e.pos()
            if(self.dragging == False):
                self.dragging = True
            else:
                self.dragging = False

        self.topBar.mouseReleaseEvent = toggleDragging
        self.topBar.mousePressEvent = toggleDragging
        self.topBar.mouseMoveEvent = drag
        self.topBar.setCursor(Qt.SizeAllCursor)

        self.window.resize(500,500)
        self.window.setLayout(self.contentContainer)
        self.window.resizeEvent = self.resize

    def close(self,e):
        self.window.close()
        self.exit()
        del self

    def open(self):
        self.window.show()
        self.run()

    def resize(self, event):
        # self.topBar.resize(event.size().width(), int(event.size().height() / 10))
        # self.exitButton.resize(self.topBar.width() /2,self.topBar.height())
        self.sizegrip.move(self.window.width() - self.sizegrip.width(),0) 

"""
app = QApplication([])
g = GUI()
g.open()
app.exec_()
app.exit()
"""
