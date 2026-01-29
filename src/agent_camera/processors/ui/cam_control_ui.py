# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cam_control.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QToolButton, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(245, 189)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(9)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 9, 0, 0)
        self.labeExposureAuto = QLabel(Form)
        self.labeExposureAuto.setObjectName(u"labeExposureAuto")

        self.gridLayout.addWidget(self.labeExposureAuto, 4, 0, 1, 1)

        self.btn_toggle_connect = QPushButton(Form)
        self.btn_toggle_connect.setObjectName(u"btn_toggle_connect")
        self.btn_toggle_connect.setAutoRepeat(False)
        self.btn_toggle_connect.setAutoDefault(False)
        self.btn_toggle_connect.setFlat(False)

        self.gridLayout.addWidget(self.btn_toggle_connect, 2, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.boxEnum = QComboBox(Form)
        self.boxEnum.setObjectName(u"boxEnum")

        self.horizontalLayout.addWidget(self.boxEnum)

        self.btn_enum_device = QToolButton(Form)
        self.btn_enum_device.setObjectName(u"btn_enum_device")

        self.horizontalLayout.addWidget(self.btn_enum_device)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.cbExposureAuto = QComboBox(Form)
        self.cbExposureAuto.addItem("")
        self.cbExposureAuto.addItem("")
        self.cbExposureAuto.setObjectName(u"cbExposureAuto")

        self.gridLayout.addWidget(self.cbExposureAuto, 4, 1, 1, 1)

        self.trigger_mode_gui = QRadioButton(Form)
        self.trigger_mode_gui.setObjectName(u"trigger_mode_gui")
        self.trigger_mode_gui.setEnabled(False)

        self.gridLayout.addWidget(self.trigger_mode_gui, 3, 0, 1, 1)

        self.leExposure = QLineEdit(Form)
        self.leExposure.setObjectName(u"leExposure")

        self.gridLayout.addWidget(self.leExposure, 5, 1, 1, 1)

        self.btn_capture = QPushButton(Form)
        self.btn_capture.setObjectName(u"btn_capture")
        self.btn_capture.setEnabled(False)

        self.gridLayout.addWidget(self.btn_capture, 3, 1, 1, 1)

        self.labeExposureTime = QLabel(Form)
        self.labeExposureTime.setObjectName(u"labeExposureTime")

        self.gridLayout.addWidget(self.labeExposureTime, 5, 0, 1, 1)


        self.retranslateUi(Form)

        self.btn_toggle_connect.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labeExposureAuto.setText(QCoreApplication.translate("Form", u"Exposure Auto", None))
        self.btn_toggle_connect.setText(QCoreApplication.translate("Form", u"K\u1ebft n\u1ed1i", None))
        self.btn_enum_device.setText(QCoreApplication.translate("Form", u"...", None))
        self.cbExposureAuto.setItemText(0, QCoreApplication.translate("Form", u"Off", None))
        self.cbExposureAuto.setItemText(1, QCoreApplication.translate("Form", u"Continuous", None))

        self.trigger_mode_gui.setText(QCoreApplication.translate("Form", u"Ch\u1ebf \u0111\u1ed9 Trigger", None))
        self.leExposure.setText(QCoreApplication.translate("Form", u"10000", None))
        self.btn_capture.setText(QCoreApplication.translate("Form", u"Ch\u1ee5p \u1ea3nh", None))
        self.labeExposureTime.setText(QCoreApplication.translate("Form", u"Exposure Time (us)", None))
    # retranslateUi

