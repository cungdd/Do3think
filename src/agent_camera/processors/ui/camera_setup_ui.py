# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_setup.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QPushButton,
    QRadioButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(174, 358)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_return = QPushButton(Form)
        self.btn_return.setObjectName(u"btn_return")

        self.verticalLayout.addWidget(self.btn_return)

        self.gbCamera = QGroupBox(Form)
        self.gbCamera.setObjectName(u"gbCamera")
        self.verticalLayout_2 = QVBoxLayout(self.gbCamera)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.hboxCameraType = QHBoxLayout()
        self.hboxCameraType.setObjectName(u"hboxCameraType")
        self.typeGige = QRadioButton(self.gbCamera)
        self.typeGige.setObjectName(u"typeGige")
        self.typeGige.setChecked(True)

        self.hboxCameraType.addWidget(self.typeGige)

        self.typeUsb = QRadioButton(self.gbCamera)
        self.typeUsb.setObjectName(u"typeUsb")

        self.hboxCameraType.addWidget(self.typeUsb)


        self.verticalLayout_2.addLayout(self.hboxCameraType)

        self.stackCamera = QStackedWidget(self.gbCamera)
        self.stackCamera.setObjectName(u"stackCamera")

        self.verticalLayout_2.addWidget(self.stackCamera)


        self.verticalLayout.addWidget(self.gbCamera)

        self.gbSetting = QGroupBox(Form)
        self.gbSetting.setObjectName(u"gbSetting")

        self.verticalLayout.addWidget(self.gbSetting)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_return.setText(QCoreApplication.translate("Form", u"Quay l\u1ea1i", None))
        self.gbCamera.setTitle(QCoreApplication.translate("Form", u"Camera", None))
        self.typeGige.setText(QCoreApplication.translate("Form", u"Gige", None))
        self.typeUsb.setText(QCoreApplication.translate("Form", u"Usb", None))
        self.gbSetting.setTitle(QCoreApplication.translate("Form", u"Th\u00f4ng s\u1ed1 c\u00e0i \u0111\u1eb7t", None))
    # retranslateUi

