import numpy as np


def RegressionNormalEquation(x, y):
    # 确保 x 和 y 是 NumPy 数组，并且转换为 float32 类型
    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)

    # 如果 x 是一维数组，将其转换为二维设计矩阵
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    # 添加截距项（在 x 的第一列添加全为 1 的列）
    x = np.hstack([np.ones((x.shape[0], 1)), x])

    # 计算正规方程
    theta = np.linalg.inv(x.T @ x) @ x.T @ y

    # 提取截距和斜率
    intercept = theta[0]
    slope = theta[1:]

    return slope, intercept


def GradientDescent(x, y, rate=1e-1, threshold=1e-6, max_iteration=1e8):

    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)

    # 添加截距项（在 x 的每一行添加一个 1）
    x = np.c_[np.ones(len(x)), x]

    # 初始化参数 theta
    theta = np.zeros(x.shape[1], dtype=np.float32)

    # 梯度下降
    for i in range(int(max_iteration)):
        # 计算预测值
        predictions = np.dot(x, theta)
        # 计算损失
        error = y - predictions
        # 计算梯度
        gradient = -np.dot(x.T, error)
        delta = np.mean(gradient ** 2)
        # 更新参数
        theta = theta - rate * gradient

        # print(f"error: {error}")
        print(f"theta: {theta}")
        print(f"grad: {gradient}")
        print(f"delta: {delta}")

        # 如果小于阈值，停止迭代
        if delta < threshold:
            break

    # 提取截距和斜率
    intercept = theta[0]
    slope = theta[1:]

    return slope, intercept
