# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TCP_Protocol.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(599, 402)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.term_rx = QTextEdit(self.tab)
        self.term_rx.setObjectName(u"term_rx")
        font = QFont()
        font.setFamilies([u"Courier New"])
        font.setPointSize(13)
        self.term_rx.setFont(font)
        self.term_rx.setStyleSheet(u"")
        self.term_rx.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.term_rx)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"min-height: 21px; min-width: 50px")

        self.verticalLayout_2.addWidget(self.pushButton, 0, Qt.AlignmentFlag.AlignRight)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout = QVBoxLayout(self.tab_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.term_tx = QTextEdit(self.tab_2)
        self.term_tx.setObjectName(u"term_tx")
        self.term_tx.setFont(font)
        self.term_tx.setStyleSheet(u"")
        self.term_tx.setReadOnly(True)

        self.verticalLayout.addWidget(self.term_tx)

        self.HLayout_tab_2 = QHBoxLayout()
        self.HLayout_tab_2.setSpacing(6)
        self.HLayout_tab_2.setObjectName(u"HLayout_tab_2")
        self.HLayout_tab_2.setContentsMargins(-1, 0, -1, -1)
        self.any_field = QLineEdit(self.tab_2)
        self.any_field.setObjectName(u"any_field")

        self.HLayout_tab_2.addWidget(self.any_field)

        self.bnSend = QPushButton(self.tab_2)
        self.bnSend.setObjectName(u"bnSend")

        self.HLayout_tab_2.addWidget(self.bnSend)

        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"min-height: 21px; min-width: 50px")

        self.HLayout_tab_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.HLayout_tab_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 3, 2, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)

        self.port_field = QSpinBox(self.groupBox)
        self.port_field.setObjectName(u"port_field")
        self.port_field.setMinimumSize(QSize(100, 0))
        self.port_field.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.port_field.setMaximum(65535)
        self.port_field.setValue(9760)

        self.gridLayout_2.addWidget(self.port_field, 0, 3, 1, 1)

        self.holderAutoConnect = QFrame(self.groupBox)
        self.holderAutoConnect.setObjectName(u"holderAutoConnect")
        self.holderAutoConnect.setFrameShape(QFrame.Shape.StyledPanel)
        self.holderAutoConnect.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.holderAutoConnect, 1, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label_3, 1, 2, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(130, 0))

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.addr_field = QHBoxLayout()
        self.addr_field.setSpacing(0)
        self.addr_field.setObjectName(u"addr_field")
        self.octet = QSpinBox(self.groupBox)
        self.octet.setObjectName(u"octet")
        self.octet.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet.setMaximum(255)
        self.octet.setValue(127)

        self.addr_field.addWidget(self.octet)

        self.dot = QLabel(self.groupBox)
        self.dot.setObjectName(u"dot")

        self.addr_field.addWidget(self.dot)

        self.octet_2 = QSpinBox(self.groupBox)
        self.octet_2.setObjectName(u"octet_2")
        self.octet_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet_2.setMaximum(255)

        self.addr_field.addWidget(self.octet_2)

        self.dot_2 = QLabel(self.groupBox)
        self.dot_2.setObjectName(u"dot_2")

        self.addr_field.addWidget(self.dot_2)

        self.octet_3 = QSpinBox(self.groupBox)
        self.octet_3.setObjectName(u"octet_3")
        self.octet_3.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet_3.setMaximum(255)

        self.addr_field.addWidget(self.octet_3)

        self.dot_3 = QLabel(self.groupBox)
        self.dot_3.setObjectName(u"dot_3")

        self.addr_field.addWidget(self.dot_3)

        self.octet_4 = QSpinBox(self.groupBox)
        self.octet_4.setObjectName(u"octet_4")
        self.octet_4.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.octet_4.setMaximum(255)
        self.octet_4.setValue(1)

        self.addr_field.addWidget(self.octet_4)


        self.gridLayout_2.addLayout(self.addr_field, 0, 1, 1, 1)

        self.labelStatus = QLabel(self.groupBox)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setMinimumSize(QSize(130, 0))
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(8)
        font1.setItalic(True)
        self.labelStatus.setFont(font1)
        self.labelStatus.setStyleSheet(u"background-color: transparent;\n"
"border: none\n"
"")
        self.labelStatus.setTextFormat(Qt.TextFormat.AutoText)

        self.gridLayout_2.addWidget(self.labelStatus, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 2, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 2, 1, 1)

        QWidget.setTabOrder(self.octet, self.octet_2)
        QWidget.setTabOrder(self.octet_2, self.octet_3)
        QWidget.setTabOrder(self.octet_3, self.octet_4)
        QWidget.setTabOrder(self.octet_4, self.port_field)
        QWidget.setTabOrder(self.port_field, self.term_tx)
        QWidget.setTabOrder(self.term_tx, self.any_field)
        QWidget.setTabOrder(self.any_field, self.bnSend)
        QWidget.setTabOrder(self.bnSend, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.term_rx)
        QWidget.setTabOrder(self.term_rx, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.tabBarClicked.connect(self.any_field.setFocus)
        self.pushButton.clicked.connect(self.term_rx.clear)
        self.pushButton_2.clicked.connect(self.term_tx.clear)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Xo\u00e1 logs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Nh\u1eadn", None))
        self.any_field.setPlaceholderText("")
        self.bnSend.setText(QCoreApplication.translate("Form", u"G\u1eedi", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Xo\u00e1 logs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"G\u01b0i", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Th\u00f4ng s\u1ed1 c\u00e0i \u0111\u1eb7t", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"C\u1ed5ng", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"T\u1ef1 \u0111\u1ed9ng k\u1ebft n\u1ed1i", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u0110\u1ecba ch\u1ec9 IP", None))
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
    # retranslateUi

