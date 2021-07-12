# -*- coding:utf-8 -*-

import sys
import math
import numpy as np
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QMainWindow, QTabWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableWidget, QItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator
from numpy.core.fromnumeric import shape

# 定义正则表达式


class Validator(QDoubleValidator):
    def __init__(self):
        """
        新坑
        创建新类
        新加三个参数，最小值，最大值，小数位数
        """
        pass


double_validator = QDoubleValidator()
double_validator.setRange(0, 10, 3)
# double_validator.setDecimals(3)
double_validator.setNotation(QDoubleValidator.StandardNotation)


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

        self.sheet = np.zeros((5, 4))
        self.initUI()

    def initUI(self):

        # 1.设置表格尺寸
        for acc_col in range(5):
            self.setColumnWidth(acc_col, 50)

        for acc_row in range(5):
            self.setRowHeight(acc_row, 20)

        # 2.设置表头
        self.setHorizontalHeaderLabels(
            ['序号', '平台(m)', '坡高(m)', '水平距(m)', '坡率'])
        for index in range(self.columnCount()):
            item = self.horizontalHeaderItem(index)
            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 3.设置表格内单元格格式
        for i in range(1, self.columnCount()):
            for j in range(self.rowCount()):

                # self.cellWidget[j][i] = QLineEdit()
                # ———————————————————明天试试这个语法可行不———————————————————
                cellwidget = QLineEdit()
                cellwidget.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

                if i == 0:
                    # 设置第一列为数字序号
                    self.setItem(j, i, QTableWidgetItem(str(j+1)))
                elif i == self.columnCount()-1:
                    # 最后一列表示斜率，这个要求数据小数位数3位，小于10
                    cellwidget.setValidator(double_validator)
                    self.setCellWidget(j, i, cellwidget)
                    cellwidget.textChanged.connect(self.update_value)
                else:
                    # 其他列表示正常
                    cellwidget.setValidator(val_double)
                    self.setCellWidget(j, i, cellwidget)
                    cellwidget.textChanged.connect(self.update_value)
                # self.item(j, i).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

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

    def get_value(self):

        return self.sheet

    def update_value(self):
        self.blockSignals(True)
        # ————————————————————blockSignals方法意义不明————————————————————
        for i in range(self.rowCount()):
            for j in range(1, self.columnCount()):
                cellwidget = self.cellWidget(i, j)
                try:
                    self.sheet[i][j] = float(cellwidget.text())
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
