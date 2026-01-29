# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_results.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(198, 247)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.chkLabel = QCheckBox(Dialog)
        self.chkLabel.setObjectName(u"chkLabel")
        self.chkLabel.setChecked(True)

        self.gridLayout.addWidget(self.chkLabel, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 8, 1, 1, 1)

        self.hboxOffsetX = QHBoxLayout()
        self.hboxOffsetX.setObjectName(u"hboxOffsetX")
        self.lblOffsetX = QLabel(Dialog)
        self.lblOffsetX.setObjectName(u"lblOffsetX")
        self.lblOffsetX.setMaximumSize(QSize(80, 16777215))

        self.hboxOffsetX.addWidget(self.lblOffsetX)

        self.sbOffsetX = QSpinBox(Dialog)
        self.sbOffsetX.setObjectName(u"sbOffsetX")
        self.sbOffsetX.setMinimum(-5000)
        self.sbOffsetX.setMaximum(5000)

        self.hboxOffsetX.addWidget(self.sbOffsetX)


        self.gridLayout.addLayout(self.hboxOffsetX, 3, 1, 1, 1)

        self.lblBox = QLabel(Dialog)
        self.lblBox.setObjectName(u"lblBox")

        self.gridLayout.addWidget(self.lblBox, 7, 1, 1, 1)

        self.hboxOffsetY = QHBoxLayout()
        self.hboxOffsetY.setObjectName(u"hboxOffsetY")
        self.lblOffsetY = QLabel(Dialog)
        self.lblOffsetY.setObjectName(u"lblOffsetY")
        self.lblOffsetY.setMaximumSize(QSize(80, 16777215))

        self.hboxOffsetY.addWidget(self.lblOffsetY)

        self.sbOffsetY = QSpinBox(Dialog)
        self.sbOffsetY.setObjectName(u"sbOffsetY")
        self.sbOffsetY.setMinimum(-5000)
        self.sbOffsetY.setMaximum(5000)

        self.hboxOffsetY.addWidget(self.sbOffsetY)


        self.gridLayout.addLayout(self.hboxOffsetY, 4, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 9, 1, 1, 1)

        self.lblConf = QLabel(Dialog)
        self.lblConf.setObjectName(u"lblConf")

        self.gridLayout.addWidget(self.lblConf, 6, 1, 1, 1)

        self.chkBox = QCheckBox(Dialog)
        self.chkBox.setObjectName(u"chkBox")
        self.chkBox.setChecked(True)

        self.gridLayout.addWidget(self.chkBox, 7, 0, 1, 1)

        self.chkConf = QCheckBox(Dialog)
        self.chkConf.setObjectName(u"chkConf")
        self.chkConf.setChecked(True)

        self.gridLayout.addWidget(self.chkConf, 6, 0, 1, 1)

        self.lblLabel = QLabel(Dialog)
        self.lblLabel.setObjectName(u"lblLabel")

        self.gridLayout.addWidget(self.lblLabel, 1, 1, 1, 1)

        self.hboxFontSize = QHBoxLayout()
        self.hboxFontSize.setObjectName(u"hboxFontSize")
        self.lblFontSize = QLabel(Dialog)
        self.lblFontSize.setObjectName(u"lblFontSize")
        self.lblFontSize.setMaximumSize(QSize(80, 16777215))

        self.hboxFontSize.addWidget(self.lblFontSize)

        self.sbFontSize = QSpinBox(Dialog)
        self.sbFontSize.setObjectName(u"sbFontSize")
        self.sbFontSize.setMinimum(1)
        self.sbFontSize.setMaximum(10)
        self.sbFontSize.setValue(3)

        self.hboxFontSize.addWidget(self.sbFontSize)


        self.gridLayout.addLayout(self.hboxFontSize, 5, 1, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Hi\u1ec3n th\u1ecb k\u1ebft qu\u1ea3", None))
        self.chkLabel.setText("")
        self.lblOffsetX.setText(QCoreApplication.translate("Dialog", u"\u0110\u1ed9 l\u1ec7ch x", None))
        self.lblBox.setText(QCoreApplication.translate("Dialog", u"H\u1ed9p", None))
        self.lblOffsetY.setText(QCoreApplication.translate("Dialog", u"\u0110\u1ed9 l\u1ec7ch y", None))
        self.lblConf.setText(QCoreApplication.translate("Dialog", u"\u0110\u1ed9 tin c\u1eady", None))
        self.chkBox.setText("")
        self.chkConf.setText("")
        self.lblLabel.setText(QCoreApplication.translate("Dialog", u"Nh\u00e3n", None))
        self.lblFontSize.setText(QCoreApplication.translate("Dialog", u"C\u1ee1 ch\u1eef", None))
    # retranslateUi

