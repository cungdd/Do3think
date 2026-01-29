# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Modbus_Protocol.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 400)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.port_field = QSpinBox(self.groupBox)
        self.port_field.setObjectName(u"port_field")
        self.port_field.setMinimumSize(QSize(100, 0))
        self.port_field.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.port_field.setMaximum(65535)
        self.port_field.setValue(9760)

        self.gridLayout_2.addWidget(self.port_field, 1, 3, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label_2, 1, 2, 1, 1)

        self.addr_field = QHBoxLayout()
        self.addr_field.setSpacing(0)
        self.addr_field.setObjectName(u"addr_field")
        self.octet = QSpinBox(self.groupBox)
        self.octet.setObjectName(u"octet")
        self.octet.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet.setMaximum(255)
        self.octet.setValue(192)

        self.addr_field.addWidget(self.octet)

        self.dot = QLabel(self.groupBox)
        self.dot.setObjectName(u"dot")

        self.addr_field.addWidget(self.dot)

        self.octet_2 = QSpinBox(self.groupBox)
        self.octet_2.setObjectName(u"octet_2")
        self.octet_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet_2.setMaximum(255)
        self.octet_2.setValue(168)

        self.addr_field.addWidget(self.octet_2)

        self.dot_2 = QLabel(self.groupBox)
        self.dot_2.setObjectName(u"dot_2")

        self.addr_field.addWidget(self.dot_2)

        self.octet_3 = QSpinBox(self.groupBox)
        self.octet_3.setObjectName(u"octet_3")
        self.octet_3.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet_3.setMaximum(255)
        self.octet_3.setValue(1)

        self.addr_field.addWidget(self.octet_3)

        self.dot_3 = QLabel(self.groupBox)
        self.dot_3.setObjectName(u"dot_3")

        self.addr_field.addWidget(self.dot_3)

        self.octet_4 = QSpinBox(self.groupBox)
        self.octet_4.setObjectName(u"octet_4")
        self.octet_4.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet_4.setMaximum(255)
        self.octet_4.setValue(10)

        self.addr_field.addWidget(self.octet_4)


        self.gridLayout_2.addLayout(self.addr_field, 1, 1, 1, 1)

        self.labelStatus = QLabel(self.groupBox)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setMinimumSize(QSize(130, 0))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(8)
        font.setItalic(True)
        self.labelStatus.setFont(font)
        self.labelStatus.setStyleSheet(u"background-color: transparent;\n"
"border: none\n"
"")
        self.labelStatus.setTextFormat(Qt.TextFormat.AutoText)

        self.gridLayout_2.addWidget(self.labelStatus, 2, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.CommunicationMode = QComboBox(self.groupBox)
        self.CommunicationMode.addItem("")
        self.CommunicationMode.setObjectName(u"CommunicationMode")

        self.gridLayout_2.addWidget(self.CommunicationMode, 0, 1, 1, 1)

        self.holderAutoConnect = QFrame(self.groupBox)
        self.holderAutoConnect.setObjectName(u"holderAutoConnect")
        self.holderAutoConnect.setFrameShape(QFrame.Shape.StyledPanel)
        self.holderAutoConnect.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.holderAutoConnect, 2, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)

        self.polling_interval = QSpinBox(self.groupBox)
        self.polling_interval.setObjectName(u"polling_interval")
        self.polling_interval.setMinimumSize(QSize(100, 0))
        self.polling_interval.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.polling_interval.setMaximum(65535)
        self.polling_interval.setValue(10)

        self.gridLayout_2.addWidget(self.polling_interval, 0, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label_3, 2, 2, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_3.addWidget(self.label_12)

        self.reg_wr_state_type = QComboBox(self.groupBox_2)
        self.reg_wr_state_type.setObjectName(u"reg_wr_state_type")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reg_wr_state_type.sizePolicy().hasHeightForWidth())
        self.reg_wr_state_type.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.reg_wr_state_type)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.reg_wr_state_addr = QSpinBox(self.groupBox_2)
        self.reg_wr_state_addr.setObjectName(u"reg_wr_state_addr")
        self.reg_wr_state_addr.setMaximum(1000)

        self.horizontalLayout_3.addWidget(self.reg_wr_state_addr)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.reg_read_type = QComboBox(self.groupBox_2)
        self.reg_read_type.setObjectName(u"reg_read_type")
        sizePolicy.setHeightForWidth(self.reg_read_type.sizePolicy().hasHeightForWidth())
        self.reg_read_type.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.reg_read_type)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.reg_read_addr = QSpinBox(self.groupBox_2)
        self.reg_read_addr.setObjectName(u"reg_read_addr")
        self.reg_read_addr.setMaximum(1000)

        self.horizontalLayout.addWidget(self.reg_read_addr)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout.addWidget(self.label_8)

        self.reg_read_value = QLineEdit(self.groupBox_2)
        self.reg_read_value.setObjectName(u"reg_read_value")
        self.reg_read_value.setReadOnly(True)

        self.horizontalLayout.addWidget(self.reg_read_value)

        self.chkAutoClear = QCheckBox(self.groupBox_2)
        self.chkAutoClear.setObjectName(u"chkAutoClear")

        self.horizontalLayout.addWidget(self.chkAutoClear)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.groupBox_2, 4, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Th\u00f4ng s\u1ed1 c\u00e0i \u0111\u1eb7t", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u0110\u1ecba ch\u1ec9 IP", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"C\u1ed5ng", None))
        self.octet.setSuffix("")
        self.octet.setPrefix("")
        self.dot.setText(QCoreApplication.translate("Form", u".", None))
        self.octet_2.setSuffix("")
        self.octet_2.setPrefix("")
        self.dot_2.setText(QCoreApplication.translate("Form", u".", None))
        self.octet_3.setSuffix("")
        self.octet_3.setPrefix("")
        self.dot_3.setText(QCoreApplication.translate("Form", u".", None))
        self.octet_4.setSuffix("")
        self.octet_4.setPrefix("")
        self.labelStatus.setText(QCoreApplication.translate("Form", u"<font color=\"red\">Disconnected</font>", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Giao th\u1ee9c", None))
        self.CommunicationMode.setItemText(0, QCoreApplication.translate("Form", u"TcpClient", None))

        self.label_5.setText(QCoreApplication.translate("Form", u"Kho\u1ea3ng c\u00e1ch \u0111\u1ecdc (ms)", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"T\u1ef1 \u0111\u1ed9ng k\u1ebft n\u1ed1i", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Thanh ghi", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Thanh ghi tr\u1ea1ng th\u00e1i", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u0110\u1ecba ch\u1ec9 b\u1eaft \u0111\u1ea7u", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u0110\u1ecdc thanh ghi          ", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u0110\u1ecba ch\u1ec9", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Gi\u00e1 tr\u1ecb hi\u1ec7n t\u1ea1i", None))
        self.reg_read_value.setText("")
        self.chkAutoClear.setText(QCoreApplication.translate("Form", u"T\u1ef1 \u0111\u1ed9ng xo\u00e1", None))
    # retranslateUi

