from PyQt5 import QtWidgets
from implementation.UI.MainWindowWithLogic import MainWindow


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec_())