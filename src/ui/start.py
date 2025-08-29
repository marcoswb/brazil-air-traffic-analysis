# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(938, 576)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(938, 522))
        self.centralwidget.setMaximumSize(QSize(938, 522))
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_1 = QFrame(self.centralwidget)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_1_1 = QFrame(self.frame_1)
        self.frame_1_1.setObjectName(u"frame_1_1")
        self.frame_1_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1_1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_1_1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.button_search_data_anac = QPushButton(self.frame_1_1)
        self.button_search_data_anac.setObjectName(u"button_search_data_anac")

        self.verticalLayout_3.addWidget(self.button_search_data_anac)

        self.button_normalize_data = QPushButton(self.frame_1_1)
        self.button_normalize_data.setObjectName(u"button_normalize_data")

        self.verticalLayout_3.addWidget(self.button_normalize_data)

        self.line = QFrame(self.frame_1_1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)


        self.horizontalLayout.addWidget(self.frame_1_1)

        self.frame_1_2 = QFrame(self.frame_1)
        self.frame_1_2.setObjectName(u"frame_1_2")
        self.frame_1_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_1_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.textedit_infos = QTextEdit(self.frame_1_2)
        self.textedit_infos.setObjectName(u"textedit_infos")
        self.textedit_infos.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.textedit_infos)


        self.horizontalLayout.addWidget(self.frame_1_2)


        self.verticalLayout.addWidget(self.frame_1)

        self.progressbar_status = QProgressBar(self.centralwidget)
        self.progressbar_status.setObjectName(u"progressbar_status")
        self.progressbar_status.setValue(0)

        self.verticalLayout.addWidget(self.progressbar_status)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 938, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_search_data_anac.setText(QCoreApplication.translate("MainWindow", u"Buscar dados ANAC", None))
        self.button_normalize_data.setText(QCoreApplication.translate("MainWindow", u"Normalizar dados", None))
    # retranslateUi

