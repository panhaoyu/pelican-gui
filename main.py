import sys
from PySide2 import QtWidgets
import ui
import core

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = ui.MainWindow()
    main_window.show()
    exit(app.exec_())
