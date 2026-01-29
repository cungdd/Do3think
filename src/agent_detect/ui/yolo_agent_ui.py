# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'yolo_agent.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QToolButton,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(242, 169)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboMode = QComboBox(Form)
        self.comboMode.addItem("")
        self.comboMode.addItem("")
        self.comboMode.setObjectName(u"comboMode")

        self.horizontalLayout_2.addWidget(self.comboMode)

        self.btnComfirm = QToolButton(Form)
        self.btnComfirm.setObjectName(u"btnComfirm")
        self.btnComfirm.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.btnComfirm)


        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 0, 1, 2)

        self.labelConf = QLabel(Form)
        self.labelConf.setObjectName(u"labelConf")
        self.labelConf.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.labelConf, 3, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(221, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 0, 1, 2)

        self.stackPanel = QStackedWidget(Form)
        self.stackPanel.setObjectName(u"stackPanel")

        self.gridLayout.addWidget(self.stackPanel, 10, 0, 1, 2)

        self.btnSelectModel = QPushButton(Form)
        self.btnSelectModel.setObjectName(u"btnSelectModel")

        self.gridLayout.addWidget(self.btnSelectModel, 2, 1, 1, 1)

        self.labelModel = QLabel(Form)
        self.labelModel.setObjectName(u"labelModel")
        self.labelModel.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.labelModel, 2, 0, 1, 1)

        self.spinConf = QSpinBox(Form)
        self.spinConf.setObjectName(u"spinConf")
        self.spinConf.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinConf.setMaximum(100)
        self.spinConf.setValue(50)

        self.gridLayout.addWidget(self.spinConf, 3, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bnThreshConfig = QPushButton(Form)
        self.bnThreshConfig.setObjectName(u"bnThreshConfig")
        self.bnThreshConfig.setStyleSheet(u"max-height: 20px;\n"
"min-height: 20px")

        self.horizontalLayout.addWidget(self.bnThreshConfig)

        self.bnResultShow = QPushButton(Form)
        self.bnResultShow.setObjectName(u"bnResultShow")
        self.bnResultShow.setStyleSheet(u"max-height: 20px;\n"
"min-height: 20px")

        self.horizontalLayout.addWidget(self.bnResultShow)


        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.comboMode.setItemText(0, QCoreApplication.translate("Form", u"Ki\u1ec3m m\u1ed1i h\u00e0n", None))
        self.comboMode.setItemText(1, QCoreApplication.translate("Form", u"Ki\u1ec3m m\u00e0u d\u00e2y", None))

        self.btnComfirm.setText("")
        self.labelConf.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.btnSelectModel.setText(QCoreApplication.translate("Form", u"Ch\u1ecdn m\u00f4 h\u00ecnh", None))
        self.labelModel.setText(QCoreApplication.translate("Form", u"M\u00f4 h\u00ecnh AI:", None))
        self.bnThreshConfig.setText(QCoreApplication.translate("Form", u"Ng\u01b0\u1ee1ng", None))
        self.bnResultShow.setText(QCoreApplication.translate("Form", u"K\u1ebft qu\u1ea3 hi\u1ec3n th\u1ecb", None))
    # retranslateUi

