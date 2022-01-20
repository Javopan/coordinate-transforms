# Form implementation generated from reading ui file 'coordinatetransform.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CoordinateTransform(object):
    def setupUi(self, CoordinateTransform):
        CoordinateTransform.setObjectName("CoordinateTransform")
        CoordinateTransform.resize(420, 80)
        CoordinateTransform.setMinimumSize(QtCore.QSize(420, 80))
        CoordinateTransform.setMaximumSize(QtCore.QSize(420, 80))
        self.verticalLayout = QtWidgets.QVBoxLayout(CoordinateTransform)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(CoordinateTransform)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txt_input = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txt_input.setFont(font)
        self.txt_input.setObjectName("txt_input")
        self.horizontalLayout.addWidget(self.txt_input)
        self.btn_transform = QtWidgets.QPushButton(self.frame)
        self.btn_transform.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_transform.setFont(font)
        self.btn_transform.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btn_transform.setAutoRepeatInterval(0)
        self.btn_transform.setObjectName("btn_transform")
        self.horizontalLayout.addWidget(self.btn_transform)
        self.verticalLayout.addWidget(self.frame)
        self.txt_output = QtWidgets.QLineEdit(CoordinateTransform)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txt_output.setFont(font)
        self.txt_output.setReadOnly(True)
        self.txt_output.setObjectName("txt_output")
        self.verticalLayout.addWidget(self.txt_output)

        self.retranslateUi(CoordinateTransform)
        QtCore.QMetaObject.connectSlotsByName(CoordinateTransform)

    def retranslateUi(self, CoordinateTransform):
        _translate = QtCore.QCoreApplication.translate
        CoordinateTransform.setWindowTitle(_translate("CoordinateTransform", "Form"))
        self.txt_input.setToolTip(_translate("CoordinateTransform", "Write a coordinate in the style of degrees minutes seconds. You can add a comma to separate Lat and Lon to have both converted at the same time. It only works for 2 coordinates."))
        self.txt_input.setPlaceholderText(_translate("CoordinateTransform", "DMS coordinate to transform"))
        self.btn_transform.setText(_translate("CoordinateTransform", "Transform"))
        self.txt_output.setToolTip(_translate("CoordinateTransform", "The output of the translation if any"))
        self.txt_output.setPlaceholderText(_translate("CoordinateTransform", "Output of the coordinate transform"))
