from PyQt5.QtWidgets import QApplication, QWidget


import sys
# 先得有QApplication这个类
# sys.argv允许创建的application使用系统命令行？
app = QApplication(sys.argv)

# 所有最高级的widgets都是窗口
window = QWidget()
window.show()

app.exec()
