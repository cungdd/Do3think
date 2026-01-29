# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'thresh_check.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(252, 265)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.hboxThreshCheck = QHBoxLayout()
        self.hboxThreshCheck.setObjectName(u"hboxThreshCheck")
        self.gbSetting = QGroupBox(Dialog)
        self.gbSetting.setObjectName(u"gbSetting")
        self.gridLayout_2 = QGridLayout(self.gbSetting)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sbBrightnessThreshold = QSpinBox(self.gbSetting)
        self.sbBrightnessThreshold.setObjectName(u"sbBrightnessThreshold")
        self.sbBrightnessThreshold.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.sbBrightnessThreshold.setMaximum(255)
        self.sbBrightnessThreshold.setSingleStep(10)
        self.sbBrightnessThreshold.setValue(100)

        self.gridLayout_2.addWidget(self.sbBrightnessThreshold, 3, 1, 1, 2)

        self.chkBrighter = QCheckBox(self.gbSetting)
        self.chkBrighter.setObjectName(u"chkBrighter")
        self.chkBrighter.setChecked(True)

        self.gridLayout_2.addWidget(self.chkBrighter, 4, 0, 1, 1)

        self.lblBrightnessThreshold = QLabel(self.gbSetting)
        self.lblBrightnessThreshold.setObjectName(u"lblBrightnessThreshold")

        self.gridLayout_2.addWidget(self.lblBrightnessThreshold, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblROI = QLabel(self.gbSetting)
        self.lblROI.setObjectName(u"lblROI")
        self.lblROI.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.lblROI)

        self.chkRoi = QCheckBox(self.gbSetting)
        self.chkRoi.setObjectName(u"chkRoi")

        self.horizontalLayout_2.addWidget(self.chkRoi, 0, Qt.AlignmentFlag.AlignHCenter)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 8, 0, 1, 3)

        self.bnGetImage = QPushButton(self.gbSetting)
        self.bnGetImage.setObjectName(u"bnGetImage")
        self.bnGetImage.setStyleSheet(u"")
        self.bnGetImage.setText(u"\ud83d\udcf8 L\u1ea5y \u1ea3nh")

        self.gridLayout_2.addWidget(self.bnGetImage, 0, 0, 1, 1)

        self.widget = QWidget(self.gbSetting)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(False)
        self.gridLayout_3 = QGridLayout(self.widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lblX1 = QLabel(self.widget)
        self.lblX1.setObjectName(u"lblX1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblX1.sizePolicy().hasHeightForWidth())
        self.lblX1.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.lblX1, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.lblX2 = QLabel(self.widget)
        self.lblX2.setObjectName(u"lblX2")
        sizePolicy.setHeightForWidth(self.lblX2.sizePolicy().hasHeightForWidth())
        self.lblX2.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.lblX2, 0, 3, 1, 1)

        self.lblY1 = QLabel(self.widget)
        self.lblY1.setObjectName(u"lblY1")
        sizePolicy.setHeightForWidth(self.lblY1.sizePolicy().hasHeightForWidth())
        self.lblY1.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.lblY1, 1, 0, 1, 1)

        self.lblY2 = QLabel(self.widget)
        self.lblY2.setObjectName(u"lblY2")
        sizePolicy.setHeightForWidth(self.lblY2.sizePolicy().hasHeightForWidth())
        self.lblY2.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.lblY2, 1, 3, 1, 1)

        self.sbX1 = QDoubleSpinBox(self.widget)
        self.sbX1.setObjectName(u"sbX1")
        self.sbX1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.sbX1, 0, 1, 1, 1)

        self.sbX2 = QDoubleSpinBox(self.widget)
        self.sbX2.setObjectName(u"sbX2")
        self.sbX2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.sbX2, 0, 4, 1, 1)

        self.sbY1 = QDoubleSpinBox(self.widget)
        self.sbY1.setObjectName(u"sbY1")
        self.sbY1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.sbY1, 1, 1, 1, 1)

        self.sbY2 = QDoubleSpinBox(self.widget)
        self.sbY2.setObjectName(u"sbY2")
        self.sbY2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout_3.addWidget(self.sbY2, 1, 4, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 9, 0, 1, 3)


        self.hboxThreshCheck.addWidget(self.gbSetting)


        self.gridLayout.addLayout(self.hboxThreshCheck, 1, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)

        QWidget.setTabOrder(self.bnGetImage, self.sbBrightnessThreshold)
        QWidget.setTabOrder(self.sbBrightnessThreshold, self.chkBrighter)
        QWidget.setTabOrder(self.chkBrighter, self.chkRoi)
        QWidget.setTabOrder(self.chkRoi, self.sbX1)
        QWidget.setTabOrder(self.sbX1, self.sbY1)
        QWidget.setTabOrder(self.sbY1, self.sbX2)
        QWidget.setTabOrder(self.sbX2, self.sbY2)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.chkRoi.toggled.connect(self.widget.setEnabled)
        self.chkRoi.toggled.connect(self.lblROI.setEnabled)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Ng\u01b0\u1ee1ng ki\u1ec3m tra", None))
        self.gbSetting.setTitle(QCoreApplication.translate("Dialog", u"Th\u00f4ng s\u1ed1", None))
        self.chkBrighter.setText(QCoreApplication.translate("Dialog", u"S\u00e1ng h\u01a1n ng\u01b0\u1ee1ng", None))
        self.lblBrightnessThreshold.setText(QCoreApplication.translate("Dialog", u"Ng\u01b0\u1ee1ng s\u00e1ng", None))
        self.lblROI.setText(QCoreApplication.translate("Dialog", u"V\u00f9ng ki\u1ec3m tra (ROI)", None))
        self.chkRoi.setText("")
        self.lblX1.setText(QCoreApplication.translate("Dialog", u"x1", None))
        self.lblX2.setText(QCoreApplication.translate("Dialog", u"x2", None))
        self.lblY1.setText(QCoreApplication.translate("Dialog", u"y1", None))
        self.lblY2.setText(QCoreApplication.translate("Dialog", u"y2", None))
        self.sbX1.setSpecialValueText("")
        self.sbX2.setSpecialValueText("")
        self.sbY1.setSpecialValueText("")
        self.sbY2.setSpecialValueText("")
    # retranslateUi

