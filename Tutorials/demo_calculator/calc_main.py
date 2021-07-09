from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .calc_interface import Ui_MainWindow
import os
import sys

global e_view

pluginsPath = 'PyQt5/Qt/plugins'
if os.path.exists(pluginsPath):
    # 指定插件路径。源码运行时不会生效，打包后运行检测到路径，加载插件
    QApplication.addLibraryPath(pluginsPath)


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def forge_link(self):
        self.b_0.clicked.connect(self.button_event(0))
        self.b_1.clicked.connect(self.button_event(1))
        self.b_2.clicked.connect(self.button_event(2))
        self.b_3.clicked.connect(self.button_event(3))
        self.b_4.clicked.connect(self.button_event(4))
        self.b_5.clicked.connect(self.button_event(5))
        self.b_6.clicked.connect(self.button_event(6))
        self.b_7.clicked.connect(self.button_event(7))
        self.b_8.clicked.connect(self.button_event(8))
        self.b_9.clicked.connect(self.button_event(9))
        self.b_add.clicked.connect(self.button_event('+'))
        self.b_sub.clicked.connect(self.button_event('-'))
        self.b_mul.clicked.connect(self.button_event('*'))
        self.b_div.clicked.connect(self.button_event('/'))
        self.b_pow.clicked.connect(self.button_event('**'))
        self.b_bra_l.clicked.connect(self.button_event('('))
        self.b_bra_r.clicked.connect(self.button_event(')'))
        self.b_mod.clicked.connect(self.button_event('%'))
        self.b_pai.clicked.connect(self.button_event('3.1415926'))
        self.b_pt.clicked.connect(self.button_event('.'))
        self.b_del.clicked.connect(self.delete_event)
        self.b_clc.clicked.connect(self.clear_event)
        self.b_eq.clicked.connect(self.calc_complish)

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.forge_link()  # 连接槽函数

    def button_event(self, arg):
        # print(dir(self.e_view))
        global e_view
        e_view = self.e_view

    def fun():  # 返回一个自定义的槽函数
        global e_view
        txt = e_view.toPlainText()
        e_view.setText(txt + str(arg))
        return fun

    def calc_complish(self):
        txt = self.e_view.toPlainText()
        ans = ''
        try:
            ans = str(eval(txt))
        except BaseException:
            ans = 'MathError'
        # print(ans)
        self.clear_event()
        self.e_view.setText(ans)
        self.l_hist.addItem(txt+'='+ans)

    def clear_event(self):
        self.e_view.setText('')

    def delete_event(self):
        txt = self.e_view.toPlainText()
        txt = txt[:len(txt)-1]
        self.e_view.setText(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec())
