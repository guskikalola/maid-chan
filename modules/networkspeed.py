#############################################
#                                           #
#                  [MODULE]                 #
#             Network ping graph            #
#                                           #
#############################################


import speedtest
import sys
import pyqtgraph as pg
import PyQt5.QtCore as  QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from pyqtgraph import PlotWidget, plot
from random import randint
from tcp_latency import measure_latency


class graph(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(graph,self).__init__(*args,**kwargs)
        
        self.graphWidget = PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.x = list(range(10))  # 100 time points
        self.y = [randint(0,10) for _ in range(10)] # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        # Add a new value 1 higher than the last.
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]  # Remove the first
        ping = int(str(measure_latency(host='8.8.8.8')).rsplit(".")[0].replace("[",""))
        print(ping)
        self.y.append(ping)  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

app = QApplication(sys.argv)
g = graph()
g.show()
sys.exit(app.exec_())
