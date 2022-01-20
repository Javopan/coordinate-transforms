from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from gui.main_window import MainWindow

import sys
import os


if __name__ == '__main__':

    app = QApplication(sys.argv)  # We define the application
    app.setStyle('Fusion')
    paleta = QPalette()
    paleta.setColor(QPalette.ColorRole.Window, QColor(43, 25, 61))
    paleta.setColor(QPalette.ColorRole.Base, QColor(166, 164, 189))
    paleta.setColor(QPalette.ColorRole.Text, QColor(242, 242, 246))
    paleta.setColor(QPalette.ColorRole.ButtonText, QColor(50, 175, 74))
    paleta.setColor(QPalette.ColorRole.Button, QColor(70, 40, 99))
    paleta.setColor(QPalette.ColorRole.Link, QColor(41, 63, 20))

    app.setPalette(paleta)

    window = MainWindow()
    window.show()  # show the window

    # start loop
    sys.exit(app.exec())
