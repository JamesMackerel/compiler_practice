from .mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication


def run():
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())