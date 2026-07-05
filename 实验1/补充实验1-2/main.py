from basic_data import *
from Newton_data import *
from src import *
import numpy as np
from matplotlib import pyplot as plt

dx = dot1.get_dx(dot2)


def SolveAndPlot(ring: NewtonRing):
    global dx
    ring.getRealData(dx)

    D2 = np.array([diameter**2 for diameter in ring.real_data])
    X = np.array([4*lamda*k for k in ring.k_list])

    # 绘制散点图
    plt.scatter(X, D2, color='blue', label='Data Points', marker='o', s=10)  # s 是点的大小

    # 拟合直线
    # coefficients = np.polyfit(X, D2, deg=1)
    # coefficients = RegressionNormalEquation(X, D2)
    coefficients = GradientDescent(X, D2)

    print(f"coe:{coefficients}")
    slope, intercept = coefficients

    line_x = np.linspace(X.min(), X.max() * 1.1, 100)  # 生成直线的 x 值
    line_y = slope * line_x + intercept  # 计算对应的 y 值

    # 绘制直线图
    plt.plot(line_x, line_y, color='red', label='Fitted Line', linestyle='--')

    # 添加标题和标签
    plt.title("Regression")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # 添加网格和图例
    plt.grid(True)
    plt.legend()

    # 显示图形
    plt.show()

    return slope, intercept


if __name__ == "__main__":
    in_key = "1"
    current_data = None

    while in_key != "e":
        in_key = str(input("输入实验数："))
        if in_key == "e":
            break
        elif in_key == "1":
            current_data = Newton_850
        elif in_key == "2":
            current_data = Newton_1000
        elif in_key == "3":
            current_data = Newton_1432
        else:
            print("Input Error!")
            continue

        slope, intercept = SolveAndPlot(current_data)
        print(f"R: {slope},  b: {intercept}")
