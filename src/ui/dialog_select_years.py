# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_select_years.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(513, 368)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_1 = QFrame(Form)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.frame_1)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_select_all = QPushButton(self.frame)
        self.button_select_all.setObjectName(u"button_select_all")

        self.horizontalLayout_2.addWidget(self.button_select_all)

        self.button_deselect_all = QPushButton(self.frame)
        self.button_deselect_all.setObjectName(u"button_deselect_all")

        self.horizontalLayout_2.addWidget(self.button_deselect_all)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_1)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.list_years = QListWidget(self.frame_2)
        self.list_years.setObjectName(u"list_years")
        self.list_years.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.verticalLayout_2.addWidget(self.list_years)


        self.verticalLayout.addWidget(self.frame_2)

        self.button_save = QPushButton(self.frame_1)
        self.button_save.setObjectName(u"button_save")

        self.verticalLayout.addWidget(self.button_save)


        self.horizontalLayout.addWidget(self.frame_1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Sele\u00e7\u00e3o de anos para download", None))
        self.button_select_all.setText(QCoreApplication.translate("Form", u"Marcar todos", None))
        self.button_deselect_all.setText(QCoreApplication.translate("Form", u"Desmarcar todos", None))
        self.button_save.setText(QCoreApplication.translate("Form", u"Salvar", None))
    # retranslateUi

