from PyQt6.QtWidgets import QWidget, QApplication
from funciones.coordinate_transform import transform
from gui.CoordinateTransform import Ui_CoordinateTransform


class CoordinateTransform(QWidget, Ui_CoordinateTransform):
    def __init__(self, parent):
        super(CoordinateTransform, self).__init__(parent)
        self.setupUi(self)

        self.btn_transform.clicked.connect(self.transform)

    def transform(self):
        input_txt_original = self.txt_input.text()
        if ',' in input_txt_original:
            coor1, coor2 = input_txt_original.split(',')
            coor1 = transform(coor1)
            coor2 = transform(coor2)
            result = f'{coor1},{coor2}'
            self.txt_output.setText(result)
            if '!' not in result:
                cb = QApplication.clipboard()
                cb.clear()
                cb.setText(result)
        else:
            coor1 = transform(input_txt_original)
            result = f'{coor1}'
            self.txt_output.setText(result)
            if '!' not in result:
                cb = QApplication.clipboard()
                cb.clear()
                cb.setText(result)


