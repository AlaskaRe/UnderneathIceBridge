# -*- coding:utf-8 -*-

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableWidget, QItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator


# 设置一些常量，例如，表格行数之类的
GLOBAL_VAR = 0
DECIMAL = 3
MAX_DIGIT = 10000

input_sheet_slope_arg = np.zeros((5, 4))
output_sheet_slope_data = np.zeros((6, 3))
support_structure_length = 0.0
slope_thickness = 0.0

# 计算坡长


def cal_slope_length(horizental: float, vertical: float, ratio: float):
    if
    elif horizental = 0:
        return vertical*(1 + ratio**2)**0.5


# 定义函数，计算output_sheet_slope_data
def update_slope_data(spt_stc_length: float, slp_thk: float, ipt_sht_slp: np.ndarray, opt_sht_slp: np.ndarray):

    for i in range(3):
        for j in range(6):
            if i == 0:
                opt_sht_slp[j][i] = ipt_sht_slp[]


# 正则表达式
val_double = QDoubleValidator()
val_double.setRange(0, MAX_DIGIT, DECIMAL)
val_double.setDecimals(DECIMAL)
val_double.setNotation(QDoubleValidator.StandardNotation)


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.setWindowTitle("Demo")

        # 创建widgets
        # Qlabel用于静态现实文字，QLineEdit输入值，QTableWidget用于表格创建
        global support_structure_length
        global slope_thickness
        self.label_supportlength = QLabel("支护长度(m)")
        self.linedit_supportlength = InputText(
            input_value=support_structure_length)

        self.label_slopethickness = QLabel("喷护厚度(mm)")
        self.linedit_slopethickness = InputText(input_value=slope_thickness)

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

        # self.setStyleSheet('')

        # 设置窗口大小不可调节
    """
    def get_updated_length(self):
        self.blockSignals(True)
        try:
            self.value_supportlength = float(self.linedit_supportlength.text())
        except ValueError:
            pass
        self.blockSignals(False)
    """


class TableInputArgsSlope(QTableWidget):

    def __init__(self):
        super(TableInputArgsSlope, self).__init__(5, 5, parent=None)

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

        # 动态获取表格内的数据
        # self.changedItem = []
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

        # print(input_sheet_slope_arg)
        self.blockSignals(False)

        """
        try:

        except ValueError:
            pass

        print(self.structed_slope_data)
        """


class EmptyDelegate(QItemDelegate):
    """该类可以保证无法修改QTableWidget中的某一列"""

    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class InputText(QLineEdit):

    def __init__(self, parent=None, input_value=0.0):

        super(InputText, self).__init__(parent)
        self.input_value = input_value
        self.setValidator(val_double)
        try:
            self.input_value = float(self.text())
        except ValueError:
            pass
        self.textChanged.connect(self.update_value)

    def update_value(self):
        # 不想再创建一个类，根据实例名字的不同来给suppoort_structure_length和slope_thickness赋值
        # 实例名叫 linedit_supportlength的就给support_structure_length赋值
        # 实例名叫 linedit_slopethickness的就给slope_thickness赋值
        # 上述想法太难了，所以弃了
        # 改为修改类，创建的时候将全局变量传递进去即可。
        self.blockSignals(True)
        try:
            self.input_value = float(self.text())
        except ValueError:
            pass
        print(self.input_value)
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
            ['序号', '支护面积（含平台）/m2', '支护面积/m2', '用料/m3'])

        # 表头格式为微软正黑体，9号字体，加粗
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

        # 3. 设置表格内单元格式
        for i in range(self.columnCount()):

            for j in range(self.rowCount()):
                # 设置表格格式

                # 3.1 设置表头
                if i == 0:
                    # 设置第一列为序号
                    self.setItem(j, i, QTableWidgetItem(str(j+1)))

                self.item(j, i).setTextAlignment(
                    Qt.AlignHCenter | Qt.AlignVCenter)

                # 3.2 设置正则表达式

        """
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
