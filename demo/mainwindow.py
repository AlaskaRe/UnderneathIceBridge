# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.setWindowTitle("Demo")

        # 创建widgets
        # Qlabel用于静态现实文字，QLineEdit输入值，QTableView用于表格创建
        self.label_supportlength = QLabel("支护长度")
        self.linedit_supportlength = QLineEdit()
        self.label_slopethickness = QLabel("喷护厚度")
        self.linedit_slopethickness = QLineEdit()
        self.table_inputargslope = TableInputArgsSlope()
        self.table_outputargslope = TableOutputArgsSlope()

        # layout
        # 整体为垂直布置，第一行为水平布置，第一行与其他widgets呈垂直布置
        whole_layout = QVBoxLayout()
        sub_layout = QHBoxLayout()

        sub_layout.addWidget(self.label_supportlength)
        sub_layout.addWidget(self.linedit_supportlength)
        sub_layout.addWidget(self.label_slopethickness)
        sub_layout.addWidget(self.linedit_slopethickness)

        whole_layout.addLayout(sub_layout)
        whole_layout.addWidget(self.table_inputargslope)
        whole_layout.addWidget(self.table_outputargslope)

        widget = QWidget()
        widget.setLayout(whole_layout)
        self.setCentralWidget(widget)


class TableInputArgsSlope(QTableView):

    def __init__(self):
        super(TableInputArgsSlope, self).__init__()
        self.setCornerButtonEnabled(True)
        self.showGrid()
        self.argsslopemodel = QStandardItemModel(5, 5)
        self.argsslopemodel.setHorizontalHeaderLabels(
            ['序号', '平台', '坡高', '水平距', '坡率'])
        self.setModel(self.argsslopemodel)


class TableOutputArgsSlope(QTableView):
    def __init__(self):
        super(TableOutputArgsSlope, self).__init__()
        self.setCornerButtonEnabled(False)
        self.showGrid()
        self.outargsslope = QStandardItemModel(6, 4)
        self.outargsslope.setHorizontalHeaderLabels(
            ['序号', '支护面积（含平台）', '支护面积', '用料'])
        sumlabel = QStandardItem("汇总")
        self.outargsslope.setItem(5, 0, sumlabel)
        self.setModel(self.outargsslope)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
