from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("My application")

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.East)
        tabs.setMovable(True)

        for n, color in enumerate(['red', 'green', 'white']):
            tabs.addTab(Color(str(color)), color)

        self.setCentralWidget(tabs)


class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

# start the event loop
app.exec_()