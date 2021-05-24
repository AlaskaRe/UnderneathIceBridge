# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableWidget, QItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor, qBlue
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.setWindowTitle("Demo")

        # 创建widgets
        # Qlabel用于静态现实文字，QLineEdit输入值，QTableWidget用于表格创建
        self.label_supportlength = QLabel("支护长度")
        self.linedit_supportlength = QLineEdit()
        self.label_slopethickness = QLabel("喷护厚度")
        self.linedit_slopethickness = QLineEdit()
        self.table_inputargslope = TableInputArgsSlope()
        # self.table_outputargslope = TableOutputArgsSlope()

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
        # whole_layout.addWidget(self.table_outputargslope)

        widget = QWidget()
        widget.setLayout(whole_layout)
        self.setCentralWidget(widget)


class TableInputArgsSlope(QTableWidget):

    def __init__(self):
        super(TableInputArgsSlope, self).__init__()
        self.setColumnCount(5)
        self.setRowCount(5)

        # 设置表格尺寸
        for acc_col in range(5):
            self.setColumnWidth(acc_col, 50)
            # self.resizeColumnsToContents()
        for acc_row in range(5):
            self.setRowHeight(acc_row, 20)

        self.setHorizontalHeaderLabels(
            ['序号', '平台', '坡高', '水平距', '坡率'])

        # 设置水平表头格式
        for index in range(self.columnCount()):
            item = self.horizontalHeaderItem(index)
            item.setFont(QFont("song", 12, QFont.Bold))
            # item.setForeground(QBrush(Qt.red))
            item.setBackground(QBrush(Qt.blue))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 设置表格无法选中
        self.setSelectionMode(QTableWidget.SingleSelection)
        # Editing starts whenever current item changes
        self.setEditTriggers(QTableWidget.CurrentChanged)
        # 单击单元格时，默认行为时选中单元格
        self.setSelectionBehavior(QTableWidget.SelectItems)
        # 不能用鼠标多选，选中单个目标
        self.setSelectionMode(QTableWidget.SingleSelection)
        # 左上角的按钮不能点击
        self.setCornerButtonEnabled(False)
        # 显示Grid
        self.setShowGrid(True)
        # 不显示垂直表头
        self.verticalHeader().setVisible(False)
        # 禁止更改列宽
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置表头(按照序号排列)
        for acc in range(1, self.columnCount()+1):
            self.setItem(acc-1, 0, QTableWidgetItem(str(acc)))
        # 设置表头不可更改
        self.setItemDelegateForColumn(0, EmptyDelegate(self))


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


"""
class TableOutputArgsSlope(QTableWidget):
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
"""

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
