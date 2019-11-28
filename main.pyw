import sys
from PySide2 import QtWidgets
import ui

# 启动程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = ui.MainWindow()
    main_window.show()
    exit(app.exec_())
