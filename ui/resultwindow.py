# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resultwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import Qt

class Ui_ResultWindow(object):
    def setupUi(self, ResultWindow):
        ResultWindow.setObjectName("ResultWindow")
        ResultWindow.resize(970, 690)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ResultWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ResultWindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lexTableWidget = QtWidgets.QTableWidget(ResultWindow)
        self.lexTableWidget.setObjectName("lexTableWidget")
        self.lexTableWidget.setColumnCount(0)
        self.lexTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.lexTableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(ResultWindow)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.quadrupleTableWidget = QtWidgets.QTableWidget(ResultWindow)
        self.quadrupleTableWidget.setObjectName("quadrupleTableWidget")
        self.quadrupleTableWidget.setColumnCount(0)
        self.quadrupleTableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.quadrupleTableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(ResultWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

    def retranslateUi(self, ResultWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "编译结果"))
        self.label.setText(_translate("ResultWindow", "词法分析结果："))
        self.label_2.setText(_translate("ResultWindow", "语义分析结果："))


class ResultWindow(QDialog, Ui_ResultWindow):
    def __init__(self, lextable, quadruple):
        super().__init__()
        self.setupUi(self)

        self.lexTableWidget.setSelectionMode(QtWidgets.QTableView.NoSelection)
        self.lexTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lexTableWidget.setRowCount(len(lextable))
        self.lexTableWidget.setColumnCount(3)
        self.lexTableWidget.setHorizontalHeaderLabels(['类型', '内容', '位置'])
        for i in range(len(lextable)):
            for j in range(3):
                self.lexTableWidget.setItem(i, j, QTableWidgetItem(str(lextable[i][j])))

        self.quadrupleTableWidget.setSelectionMode(QtWidgets.QTableView.NoSelection)
        self.quadrupleTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.quadrupleTableWidget.setRowCount(len(quadruple))
        self.quadrupleTableWidget.setColumnCount(4)
        self.quadrupleTableWidget.setHorizontalHeaderLabels(['运算符', '参数1', '参数2', '结果'])
        for i in range(len(quadruple)):
            for j in range(4):
                self.quadrupleTableWidget.setItem(i, j, QTableWidgetItem(str(quadruple[i][j])))
