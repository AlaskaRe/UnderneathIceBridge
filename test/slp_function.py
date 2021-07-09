import math
import numpy as np


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

    else:
        return math.sqrt(horizental**2+vertical**2)


def update_slope_data(spt_stc_length: float, slp_thk: float, ipt_sht_slp: np.ndarray(shape=(5, 4)), opt_sht_slp: np.ndarray(shape=(6, 4))):

    # 定义函数，计算output_sheet_slope_data

    for j in range(5):
        net_slp = cal_slope_length(
            ipt_sht_slp[j][2], ipt_sht_slp[j][1], ipt_sht_slp[j][3])

        opt_sht_slp[j][0] = net_slp + ipt_sht_slp[j][0]
        opt_sht_slp[j][1] = net_slp
        opt_sht_slp[j][2] = spt_stc_length * slp_thk * opt_sht_slp[j][0]
        opt_sht_slp[j][3] = spt_stc_length * slp_thk * opt_sht_slp[j][1]

    # https://blog.csdn.net/u014636245/article/details/84181868
    # https://blog.csdn.net/weixin_39975529/article/details/111678130
    # https://www.jianshu.com/p/7a0d9e726c22
    # https://numpy.org/doc/stable/user/quickstart.html#prerequisites

    sum_last_row = np.sum(opt_sht_slp, axis=0)
    j = 0
    for i in sum_last_row:
        opt_sht_slp[5][j] = i
        j += 1


# c = cal_slope_length(1, , 1)
a = np.array([[1, 1, 1, 1], [1, 0, 1, 1], [
             1, 1, 0, 1], [1, 1, 1, 0], [1, 0, 0, 1]])

length = 100
thickness = 5

b = np.zeros((6, 4))

update_slope_data(length, thickness, a, b)
print(b)
