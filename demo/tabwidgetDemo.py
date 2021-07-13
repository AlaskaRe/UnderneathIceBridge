# -*- coding:utf-8 -*-


import sys
import math
import numpy as np
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QHeaderView, QMainWindow, QTabWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableWidget, QItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator
from numpy.core.fromnumeric import shape

# 定义一些常量
DECIMAL = 3

# 定义一些线程，对于slopeInterface类，应该需要三个线程
# 1.支护长度线程
# 2.支护厚度线程
# 3.放坡参数线程
# 这三个线程其中一个启动之后，会调用其他两个线程，调用之后，启动计算函数


class DigitValidator(QDoubleValidator):
    def __init__(self, mindigit, maxdigit, dot):
        """
        新坑
        创建新类
        新加三个参数，最小值，最大值，小数位数
        class 子类名(父类名)：
            def __init__(self, 参数表， 新的属性)：
                super().__init__(参数表)
                self.新的属性 = 新的属性

            def 重定义方法（self, 参数表）：
        """
        super(DigitValidator, self).__init__()

        self.mindigit = mindigit
        self.maxdigit = maxdigit
        self.dot = dot

        self.setRange(self.mindigit, self.maxdigit, self.dot)
        self.setNotation(QDoubleValidator.StandardNotation)


class EmptyDelegate(QItemDelegate):
    """该类可以保证无法修改QTableWidget中的某一列"""

    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


ratio_validator = DigitValidator(0, 10, DECIMAL)
ordnary_validator = DigitValidator(0, 10000, DECIMAL)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('TabWidgetDemo')

        # 创建QTabWidget
        self.tabwidget = TabPage()
        self.setCentralWidget(self.tabwidget)


class TabPage(QTabWidget):
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
        self.linedit_supportlength = InputText()

        self.label_slopethickness = QLabel("喷护厚度/m")
        self.linedit_slopethickness = InputText()

        self.inputsheet = TableInputArgsSlope()
        self.outputsheet = TableOutputArgsSlope()

        self.do_layout()

    def do_layout(self):
        up_layout = QVBoxLayout()
        sub_layout = QHBoxLayout()

        sub_layout.addWidget(self.label_supportlength)
        sub_layout.addWidget(self.linedit_supportlength)
        sub_layout.addWidget(self.label_slopethickness)
        sub_layout.addWidget(self.linedit_slopethickness)

        up_layout.addLayout(sub_layout)
        up_layout.addWidget(self.inputsheet)
        up_layout.addWidget(self.outputsheet)
        self.setLayout(up_layout)


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

        # 3.设置表格内单元格及格式
        for i in range(self.columnCount()):
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
                    cellwidget.setValidator(ratio_validator)
                    self.setCellWidget(j, i, cellwidget)
                    cellwidget.textChanged.connect(self.update_value)
                    # 此处也该启动线程，发送信号，信号包含sheet数据
                else:
                    # 其他列数据要求，小于10000，小数位数3位
                    cellwidget.setValidator(ordnary_validator)
                    self.setCellWidget(j, i, cellwidget)
                    cellwidget.textChanged.connect(self.update_value)
                    # 此处也该启动线程，发送信号，信号包含sheet数据
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
        #   设置表头不可更改
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
        self.sheet = np.zeros((6, 4))
        self.initUI()
        self.insert_sheet()

    def initUI(self):
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

        # 3. 设置表格内单元及格式
        for i in range(self.columnCount()):
            for j in range(self.rowCount()):
                if i == 0:
                    # 设置第一列为序号
                    # 第一列最后一个为汇总
                    self.setItem(j, i, QTableWidgetItem(str(j+1)))
                    if j == 5:
                        self.setItem(j, i, QTableWidgetItem('汇总'))
                else:
                    self.setItem(j, i, QTableWidgetItem('0'))
                self.item(j, i).setTextAlignment(
                    Qt.AlignHCenter | Qt.AlignVCenter)

        # 4.限制表格行为
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

    def get_value(self):
        """
        返回数组
        """
        return self.sheet

    def insert_sheet(self):
        """
        将数组sheet写入显示列表
        """
        for i in range(6):
            for j in range(4):
                inner_data = round(self.sheet[i][j], DECIMAL)
                self.setItem(i, j+1, QTableWidgetItem(str(inner_data)))

    def update_value(self):
        pass


class TableEarthNail(QTableWidget):

    def __init__(self):
        super(TableEarthNail, self).__init__(15, 5, parent=None)
        self.sheet = np.zeros((15, 4))
        self.initUI()

    def initUI(self):

        # 1.设置表格尺寸
        for acc_col in range(self.columnCount()):
            self.setColumnWidth(acc_col, 50)
        for acc_row in range(self.rowCount()):
            self.setRowHeight(acc_row, 20)

        # 2设置表头及格式
        self.setHorizontalHeaderLabels(
            ['序号', '单根长度/m', '水平间距/m', '材料类型', '总长度'])
        for index in range(self.columnCount()):
            item = self.horizontalHeaderItem(index)
            item.setFont(QFont("Microsoft JhengHei", 9, QFont.Bold))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 3.设置表格内单元及格式
        for i in range(self.columnCount()):
            for j in range(self.rowCount()):
                if i == 0:
                    # 设置第一列为序号
                    self.setItem(j, i, QTableWidgetItem(str(j+1)))
                elif i == 3:

                    # 设置为下拉菜单选项
                    earthnail_combox = QComboBox()
                    earthnail_combox.addItem(['钢筋', '锚索', '锚杆'])
                    self.setItem(j, i, earthnail_combox)
                    # earthnail_combox.currentIndexChanged.connect()
                else:
                    pass


class InputText(QLineEdit):

    def __init__(self, parent=None):

        super(InputText, self).__init__(parent)
        self.input_value = 0

        self.setValidator(ordnary_validator)
        self.textChanged.connect(self.update_value)

        # 线程启动，传出数据，调用函数
        # self.textChanged.connect(slopeprogress.start)

    def get_value(self):
        return self.input_value

    def update_value(self):
        self.blockSignals(True)
        try:
            self.input_value = float(self.text())
        except ValueError:
            pass
        self.blockSignals(False)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
