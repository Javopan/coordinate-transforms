from PyQt6.QtWidgets import QWidget, QTextEdit, QGridLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class Licensing(QWidget):
    psig_aceptado = pyqtSignal(bool)  # Signal that the license was shown boolean

    def __init__(self, button=None, parent=None):
        super(Licensing, self).__init__(parent=parent)

        message = """<p>This is a free tool under the GPL v 3.</p>
                  <p>This software uses the following tools:</p>
                  <p>-<a href='https://riverbankcomputing.com/commercial/pyqt'>PyQT6</a><br>
                  -<a href='https://github.com/mapado/haversine'>Haversine</a><br>
                  -<a href='https://www.crummy.com/software/BeautifulSoup/'>Beautiful Soup 4</a><br>
                  -<a href='https://pandas.pydata.org'>Pandas</a><br>
                  <p>We use the folowing icons:</p>
                  -<a href='https://p.yusukekamiyamane.com'>Fugue Icons</a> by Yusuke Kamiyamane
                  -<a href='https://github.com/ionic-team/ionicons'>ionicons</a>
                  <p>We use the following frameworks:</p>
                  -<a href='https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI'>Wanderson Magalhaes modified themes</a>"""

        txt_texto = QTextEdit(message)
        if button:
            btn_aceptar = QPushButton('Entendido')
            btn_aceptar.clicked.connect(self.aceptado)

        layout = QGridLayout()
        layout.addWidget(txt_texto, 0, 0, 1, 1)
        if button:
            layout.addWidget(btn_aceptar, 1, 0, 1, 1)

        self.setLayout(layout)

    def aceptado(self):
        self.psig_aceptado.emit(True)
