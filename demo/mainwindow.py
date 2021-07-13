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


# 设置一些常量，例如，表格行数之类的
GLOBAL_VAR = 0
DECIMAL = 3
MAX_DIGIT = 10000

input_sheet_slope_arg = np.zeros((5, 4))
output_sheet_slope_data = np.zeros((6, 4))
support_structure_length = 0.0
slope_thickness = 0.0


def cal_slope_length(horizental: float, vertical: float, ratio: float):
    # 计算坡长

    # 这就涉及到一个问题，检测输入的参数（水平距离、 垂直距离、斜率）是否有效
    # 在此，本程序的设计理念：
    # 1.三者为0，则坡长为0
    # 2.三者有任意两参数不为0，则坡长不为0
    # ————————————————————————————————————————————————————————————————————————————————————————————————————
    # 3.三个参数都不为0，计算这组数据是否有效——斜率是否与水平距离、垂直距离相匹配，不匹配自动更正，下次改进
    # ————————————————————————————————————————————————————————————————————————————————————————————————————
    # 3.三个参数都不为0，则根据水平距离、垂直距离来进行计算坡长，忽略斜率是否是有效的
    # 4.问题
    # 如果传入的参数有一个为空，则报错
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

    # 定义函数，计算output_sheet_slope_data
    for i in range(4):
        opt_sht_slp[5][i] = 0.0

    for j in range(5):
        net_slp = cal_slope_length(
            ipt_sht_slp[j][2], ipt_sht_slp[j][1], ipt_sht_slp[j][3])

        opt_sht_slp[j][0] = (net_slp + ipt_sht_slp[j][0])*spt_stc_length
        opt_sht_slp[j][1] = net_slp * spt_stc_length
        opt_sht_slp[j][2] = (spt_stc_length * slp_thk * opt_sht_slp[j][0])/1000
        opt_sht_slp[j][3] = (spt_stc_length * slp_thk * opt_sht_slp[j][1])/1000

    # https://blog.csdn.net/u014636245/article/details/84181868
    # https://blog.csdn.net/weixin_39975529/article/details/111678130
    # https://www.jianshu.com/p/7a0d9e726c22
    # https://numpy.org/doc/stable/user/quickstart.html#prerequisites

    sum_last_row = np.sum(opt_sht_slp, axis=0)
    for i in range(4):
        opt_sht_slp[5][i] = sum_last_row[i]


def cal_earth_nail(spt_stc_length: float, ipt_sht_earth_nail: np.ndarray(shape=(15, 4))):
    # 新坑，ipt_sht_earth_nail是个[15][4]数组，最后一列数组的数据类型为文本型

    pass


# 正则表达式
val_double = QDoubleValidator()
val_double.setRange(0, MAX_DIGIT, DECIMAL)
val_double.setDecimals(DECIMAL)
val_double.setNotation(QDoubleValidator.StandardNotation)


class Progress(QThread):

    # https://stackoverflow.com/questions/3756510/pyqt-pyobject-equivalent-when-using-new-style-signals-slots
    cal_signal = pyqtSignal()

    def __init__(self, parent=None):
        # https://www.ddpool.cn/article/77285.html
        # https://blog.csdn.net/jia666666/article/details/81674427
        # https://www.jb51.net/article/163258.htm
        super(Progress, self).__init__(parent)

    def run(self):
        global input_sheet_slope_arg
        global output_sheet_slope_data
        global support_structure_length
        global slope_thickness
        update_slope_data(support_structure_length, slope_thickness,
                          input_sheet_slope_arg, output_sheet_slope_data)

        self.cal_signal.emit()
        # self.sleep(1)


class EmptyDelegate(QItemDelegate):
    """该类可以保证无法修改QTableWidget中的某一列"""

    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.setWindowTitle("Demo")

        # 创建widgets
        # Qlabel用于静态现实文字，QLineEdit输入值，QTableWidget用于表格创建
        global support_structure_length
        global slope_thickness
        self.label_supportlength = QLabel("支护长度(m)")
        self.linedit_supportlength = LengthInputText()

        self.label_slopethickness = QLabel("喷护厚度(mm)")
        self.linedit_slopethickness = ThickInputText()

        self.table_inputargslope = TableInputArgsSlope()

        self.table_outputargslope = TableOutputArgsSlope()
        # 自动更新计算结果
        slopeprogress.cal_signal.connect(
            self.table_outputargslope.update_data)

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
        # whole_layout.addWidget(self.table_outputargslope)
        """"""
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

        # print(input_sheet_slope_arg)
        self.blockSignals(False)

        """
        try:

        except ValueError:
            pass

        print(self.structed_slope_data)
        """


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


slopeprogress = Progress()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
