import sys

import PyQt5.sip
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from ui.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = MainWindow(app)
    win.show()

    sys.exit(app.exec_())
