# -*- coding:utf-8 -*-


import sys
import math
import numpy as np
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QHeaderView, QMainWindow, QTabWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit,  QTableWidget, QItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush, QColor
from PyQt5.QtCore import QLine, Qt, QThread, pyqtSignal
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator
from numpy.core.fromnumeric import shape

# 定义常量
DECIMAL = 3


def cal_slope_length(horizental: float, vertical: float, ratio: float):

    a = horizental == 0
    b = vertical == 0
    c = ratio == 0
    anti_ratio = 0
    if a and b and c:
        return 0

    elif (a and b) or (a and c) or (b and c):
        return 0

    elif (not a) and (not b) and (not c):
        return math.sqrt(horizental**2+vertical**2)

    elif a:
        return vertical*math.sqrt((1 + ratio**2))

    elif b:
        try:
            anti_ratio = 1/ratio
        except ZeroDivisionError:
            return 0
        return horizental * math.sqrt(1 + anti_ratio**2)

    elif c:
        return math.sqrt(horizental**2+vertical**2)


def update_slope_data(spt_stc_length: float, slp_thk: float, ipt_sht_slp: np.ndarray(shape=(5, 4)), opt_sht_slp: np.ndarray(shape=(6, 4))):

    # 计算output_sheet_slope_data
    for i in range(4):
        opt_sht_slp[5][i] = 0.0

    for j in range(5):
        net_slp = cal_slope_length(
            ipt_sht_slp[j][2], ipt_sht_slp[j][1], ipt_sht_slp[j][3])

        opt_sht_slp[j][0] = (net_slp + ipt_sht_slp[j][0])*spt_stc_length
        opt_sht_slp[j][1] = net_slp * spt_stc_length
        opt_sht_slp[j][2] = (spt_stc_length * slp_thk * opt_sht_slp[j][0])/1000
        opt_sht_slp[j][3] = (spt_stc_length * slp_thk * opt_sht_slp[j][1])/1000

    sum_last_row = np.sum(opt_sht_slp, axis=0)
    for i in range(4):
        opt_sht_slp[5][i] = sum_last_row[i]


def cal_earth_nail_length(spt_stc_length: float, earth_nail_sheet: np.ndarray(shape=(15, 2)), earth_nail_sum: np.ndarray((15, 1))):

    try:
        for i in range(15):
            earth_nail_sum[i][0] = (
                math.ceil(spt_stc_length/earth_nail_sheet[i][1])+1)*earth_nail_sheet[i][0]
    except OverflowError:
        pass


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
        self.earthnailpage = EarthNailInterface()

        # 将选项卡添加到顶层窗口中
        self.addTab(self.slopepage, "放坡支护")
        self.addTab(self.earthnailpage, "土钉支护")


class SlopeInterface(QWidget):
    def __init__(self):
        super(SlopeInterface, self).__init__()

        self.length = 0
        self.thickness = 0
        self.slopeargs = np.zeros((5, 4))
        self.quantity = np.zeros((6, 4))

        self.initUI()
        self.make_connection()

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

    def make_connection(self):

        self.linedit_supportlength.textChanged.connect(self.update_length)
        self.linedit_slopethickness.textChanged.connect(
            self.update_thickness)
        self.inputsheet.valueChanged.connect(self.update_slopeargs)

    def update_length(self):
        """
        更新self.length并调用update_quantity()方法更新self.quantity
        """
        self.length = self.linedit_supportlength.get_value()
        self.update_quantity()

    def update_thickness(self):
        self.thickness = self.linedit_slopethickness.get_value()
        self.update_quantity()

    def update_slopeargs(self):
        self.slopeargs = self.inputsheet.get_value()
        self.update_quantity()

    def update_quantity(self):
        """
        计算工作量
        并将工作量结果插入表格中
        计算结果传入self.outputsheet.sheet中
        并调用其inset_value()方法
        """
        update_slope_data(self.length, self.thickness,
                          self.slopeargs, self.quantity)
        self.outputsheet.sheet = self.quantity
        self.outputsheet.insert_sheet()


class EarthNailInterface(QWidget):
    def __init__(self):
        super(EarthNailInterface, self).__init__()
        self.length = 0
        self.thickness = 0
        self.earthnailargs = np.zeros((15, 2))
        self.earthnailtotal = np.zeros((15, 1))

        self.initUI()
        self.make_connection()

    def initUI(self):
        self.label_supportlength = QLabel("支护长度/m")
        self.linedit_supportlength = InputText()

        self.label_slopethickness = QLabel("喷护厚度/m")
        self.linedit_slopethickness = InputText()

        self.interfacesheet = TableEarthNail()

        self.do_layout()

    def do_layout(self):
        up_layout = QVBoxLayout()
        sub_layout = QHBoxLayout()

        sub_layout.addWidget(self.label_supportlength)
        sub_layout.addWidget(self.linedit_supportlength)
        sub_layout.addWidget(self.label_slopethickness)
        sub_layout.addWidget(self.linedit_slopethickness)

        up_layout.addLayout(sub_layout)
        up_layout.addWidget(self.interfacesheet)

        self.setLayout(up_layout)

    def make_connection(self):

        self.linedit_supportlength.textChanged.connect(
            self.update_struct_length)
        self.linedit_slopethickness.textChanged.connect(
            self.update_slopethickness)
        self.interfacesheet.valueChanged.connect(self.update_sumlength)

    def update_struct_length(self):
        self.length = self.linedit_supportlength.get_value()
        self.update_sumlength()

    def update_slopethickness(self):
        self.thickness = self.linedit_slopethickness.get_value()
        self.update_sumlength()

    def update_sumlength(self):
        self.earthnailargs = self.interfacesheet.get_args()
        cal_earth_nail_length(
            self.length, self.earthnailargs, self.earthnailtotal)
        self.interfacesheet.sumlength = self.earthnailtotal
        self.interfacesheet.update_sum()


class AnchorCalbleInterface(QWidget):
    def __init__(self):
        super(AnchorCalbleInterface, self).__init__()
        self.initUI()
        # self.sheet= np.zeros()

    def initUI(self):

        self.do_layout()

    def do_layout(self):
        pass


class TableInputArgsSlope(QTableWidget):

    valueChanged = pyqtSignal()

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

        for i in range(self.rowCount()):
            for j in range(1, self.columnCount()):
                cellwidget = self.cellWidget(i, j)
                try:
                    self.sheet[i][j-1] = float(cellwidget.text())
                except ValueError:
                    pass
        self.valueChanged.emit()


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

    valueChanged = pyqtSignal()

    def __init__(self):
        super(TableEarthNail, self).__init__(15, 5, parent=None)
        self.args_sheet = np.zeros((15, 2))
        self.sumlength = np.zeros((15, 1))
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
                    earthnail_combox.addItems(['钢筋', '锚索', '锚杆'])
                    self.setCellWidget(j, i, earthnail_combox)
                    # earthnail_combox.currentIndexChanged.connect()
                elif i == 4:
                    sum = str(self.sumlength[j][0])
                    self.setItem(j, i, QTableWidgetItem(sum))
                else:
                    cellwidget = QLineEdit()
                    cellwidget.setValidator(ordnary_validator)
                    self.setCellWidget(j, i, cellwidget)
                    cellwidget.textChanged.connect(self.update_args)

        # 4.限制表格行为
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
        #   设置最后一列不可更改
        self.setItemDelegateForColumn(4, EmptyDelegate(self))

    def get_sum(self):
        return self.sumlength

    def get_args(self):
        return self.args_sheet

    def update_sum(self):
        """
        表格内前两列数据发生变化，即更新最后一列
        并将更新后的数据写入显示的表格中
        """
        for i in range(15):
            data = str(self.sumlength[i][0])
            self.setItem(i, 4, QTableWidgetItem(data))

    def update_args(self):

        for i in range(self.rowCount()):
            try:
                single_length = float(self.cellWidget(i, 1).text())
                self.args_sheet[i][0] = single_length
                horizontial_gap = float(self.cellWidget(i, 2).text())
                self.args_sheet[i][1] = horizontial_gap
            except ValueError:
                pass

        self.valueChanged.emit()


class InputText(QLineEdit):

    def __init__(self, parent=None):

        super(InputText, self).__init__(parent)
        self.input_value = 0

        self.setValidator(ordnary_validator)
        self.textChanged.connect(self.update_value)

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
