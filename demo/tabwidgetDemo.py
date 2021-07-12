# -*- coding:utf-8 -*-

from _typeshed import IdentityFunction
import sys
import math
import numpy as np
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QMainWindow, QTabWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableWidget, QItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator
from numpy.core.fromnumeric import shape


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('TabWidgetDemo')

        # 创建QTabWidget
        self.tabwidget = TabPage()


class TabPage(QTableWidget):
    def __init__(self):
        super(TabPage, self).__init__()

        # 创建选项卡窗口
        self.slopepage = SlopeInterface()

        # 将选项卡添加到顶层窗口中
        self.addTab(self.slopepage, "放坡支护")


class SlopeInterface(QWidget):
    def __init__(self):
        super(SlopeInterface, self).__init__()
        self.initUI()

    def initUI(self):
        self.label_supportlength = QLabel("支护长度/m")
        self.linedit_supportlength = LengthInputText()

        self.label_slopethickness = QLabel("喷护厚度/m")
        self.linedit_supportlength = LengthInputText()
        self.inputsheet = TableInputArgsSlope()
        self.outputsheet = TableOutputArgsSlope()

        self.do_layout()

    def do_layout(self):
        up_layout = QVBoxLayout()
        sub_layout = QHBoxLayout()

        sub_layout.addWidget(self.label_supportlength)
        sub_layout.addWidget(self.linedit_supportlength)
        sub_layout.addWidget(self.label_slopethickness)
        sub_layout.addWidget(self.label_slopethickness)

        up_layout.addLayout(sub_layout)
        up_layout.addWidget(self.inputsheet)
        up_layout.addWidget(self.outputsheet)


class TableInputArgsSlope(QTableWidget):

    def __init__(self):
        super(TableInputArgsSlope, self).__init__(5, 5, parent=None)

        # 教程
        # https://blog.csdn.net/zhulove86/article/details/52599738
        # https://blog.csdn.net/panrenlong/article/details/79959069
        # 1设置表格尺寸
        for acc_col in range(5):
            self.setColumnWidth(acc_col, 50)
            # self.resizeColumnsToContents()
        for acc_row in range(5):
            self.setRowHeight(acc_row, 20)

        self.setHorizontalHeaderLabels(
            ['序号', '平台(m)', '坡高(m)', '水平距(m)', '坡率'])

        # 2.设置水平表头格式
        #   表头为微软正黑体，9号字体，加粗
        for index in range(self.columnCount()):

            item = self.horizontalHeaderItem(index)
            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            # 设置背景颜色不起作用
            # item.setForeground(QBrush(QColor(128, 255, 0)))
            # --------------------------------------------------------
            # 这个function不起作用，先空着
            item.setBackground(QBrush(Qt.red))
            # -------------------------------------------------------
            # self.setAutoFillBackground(True)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 3.设置表格内单元格格式
        #   ________________
        #   没找到怎么设置数据类型的方法，只好用正则表达式来顶替下

        for i in range(self.columnCount()):
            for j in range(self.rowCount()):
                # 设置表格格式
                # setItem之后，才能对其进行格式设置

                # 3.1设置表头
                if i == 0:
                    self.setItem(j, i, QTableWidgetItem(str(j+1)))
                    self.item(j, i).setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
                # 3.2设置正则表达式,表示数字
                elif i == self.columnCount()-1:
                    val_double_2 = QDoubleValidator()
                    val_double_2.setRange(0, 10, DECIMAL)
                    val_double_2.setDecimals(DECIMAL)
                    val_double_2.setNotation(QDoubleValidator.StandardNotation)
                    cellwidget_slope_rate = QLineEdit()
                    cellwidget_slope_rate.setAlignment(
                        Qt.AlignVCenter | Qt.AlignHCenter)
                    cellwidget_slope_rate.setValidator(val_double_2)
                    self.setCellWidget(j, i, cellwidget_slope_rate)

                    cellwidget_slope_rate.textChanged.connect(self.get_updated)
                    cellwidget_slope_rate.textChanged.connect(
                        slopeprogress.start)
                else:
                    # reg_digit = QRegExp("(\d)+")
                    # validator_digit = QRegExpValidator(reg_digit)

                    cellwidget = QLineEdit()
                    cellwidget.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    # cellwidget.setValidator(validator_digit)
                    cellwidget.setValidator(val_double)
                    self.setCellWidget(j, i, cellwidget)
                    # self.cellWidget(j, i).setText("1")

                    cellwidget.textChanged.connect(self.get_updated)
                    cellwidget.textChanged.connect(slopeprogress .start)
                    # print(self.structed_slope_data)

        # 4.其他项设置，限制表格行为
        #   设置表格无法选中
        self.setSelectionMode(QTableWidget.SingleSelection)
        #   Editing starts whenever current item changes
        self.setEditTriggers(QTableWidget.CurrentChanged)
        #   单击单元格时，默认行为时选中单元格
        self.setSelectionBehavior(QTableWidget.SelectItems)
        #   不能用鼠标多选，选中单个目标
        self.setSelectionMode(QTableWidget.SingleSelection)
        #   左上角的按钮不能点击
        self.setCornerButtonEnabled(False)
        #   显示Grid
        self.setShowGrid(True)
        #   不显示垂直表头
        self.verticalHeader().setVisible(False)
        #   禁止更改列宽
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置表头不可更改
        self.setItemDelegateForColumn(0, EmptyDelegate(self))

    def get_updated(self):
        """表格内的内容有变更，即更新数组"""
        global input_sheet_slope_arg

        self.blockSignals(True)
        for i in range(1, self.columnCount()):
            for j in range(self.rowCount()):
                cellwidget_lineedit = self.cellWidget(j, i)
                try:
                    input_sheet_slope_arg[j][i -
                                             1] = float(cellwidget_lineedit.text())

                except ValueError:
                    pass

        self.blockSignals(False)


class TableOutputArgsSlope(QTableWidget):
    def __init__(self):
        super(TableOutputArgsSlope, self).__init__(6, 5, parent=None)
        # 1 设置表格尺寸
        for acc_col in range(6):
            self.setColumnWidth(acc_col, 50)
        for acc_row in range(5):
            self.setRowHeight(acc_row, 20)

        # 2. 设置表头及格式
        self.setHorizontalHeaderLabels(
            ['序号', '支护面积（含平台）/m2', '支护面积/m2', '用料(含平台)/m3', '用料(不含平台)/m3'])

        # 表头格式为微软正黑体，9号字体，加粗
        for index in range(self.columnCount()):
            item = self.horizontalHeaderItem(index)
            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 3. 设置表格内单元格式
        for i in range(self.columnCount()):

            for j in range(self.rowCount()):
                # 设置表格格式
                global output_sheet_slope_data
                # 3.1 设置表头
                if i == 0:
                    # 设置第一列为序号
                    self.setItem(j, i, QTableWidgetItem(str(j+1)))
                    if j == 5:

                        self.setItem(j, i, QTableWidgetItem('汇总'))
                else:
                    self.update_data()

                # self.item(j, i).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 限制表格行为

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.setSelectionMode(QTableWidget.SingleSelection)
        #   左上角的按钮不能点击
        self.setCornerButtonEnabled(False)
        #   显示Grid
        self.setShowGrid(True)
        #   不显示垂直表头
        self.verticalHeader().setVisible(False)
        #   禁止更改列宽
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_data(self):
        # 这里需要用到线程，动态的获取全局变量output_sheet_slope_data更新显示
        global output_sheet_slope_data
        for i in range(6):
            for j in range(4):
                # 此处涉及到这个数组的数据小数位数问题
                inner_data = round(
                    output_sheet_slope_data[i][j], DECIMAL)
                self.setItem(i, j+1, QTableWidgetItem(str(inner_data)))


class LengthInputText(QLineEdit):

    def __init__(self, parent=None):

        super(LengthInputText, self).__init__(parent)
        # self.input_value = input_value
        self.setValidator(val_double)
        try:
            self.input_value = float(self.text())
        except ValueError:
            pass
        self.textChanged.connect(self.update_value)
        self.textChanged.connect(slopeprogress.start)

    def update_value(self):
        # 不想再创建一个类，根据实例名字的不同来给suppoort_structure_length和slope_thickness赋值
        # 实例名叫 linedit_supportlength的就给support_structure_length赋值
        # 实例名叫 linedit_slopethickness的就给slope_thickness赋值
        # 上述想法太难了，所以弃了
        # 改为修改类，创建的时候将全局变量传递进去即可。
        self.blockSignals(True)
        global support_structure_length
        try:
            support_structure_length = float(self.text())
        except ValueError:
            pass
        # print(self.input_value)
        self.blockSignals(False)


class ThickInputText(QLineEdit):

    def __init__(self, parent=None):

        super(ThickInputText, self).__init__(parent)
        # self.input_value = input_value
        self.setValidator(val_double)
        try:
            self.input_value = float(self.text())
        except ValueError:
            pass
        self.textChanged.connect(self.update_value)
        self.textChanged.connect(slopeprogress.start)

    def update_value(self):
        self.blockSignals(True)
        global slope_thickness
        try:
            slope_thickness = float(self.text())
        except ValueError:
            pass
        # print(self.input_value)
        self.blockSignals(False)
