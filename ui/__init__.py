from .mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

def run():
    import sys
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())