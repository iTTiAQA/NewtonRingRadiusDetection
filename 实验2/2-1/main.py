import numpy as np
import matplotlib.pyplot as plt

# 参数设置
A = 1.0  # 振幅
f0 = 1.0  # 初始频率
f1 = 10.0  # 终止频率
T = 1.0  # 信号持续时间
fs = 1000  # 采样频率
t = np.linspace(0, T, int(T * fs), endpoint=False)


# 生成Chirp信号
def chirp_signal(t, f0, f1, phi0):
    f = f0 + (f1 - f0) * t / T
    return A * np.cos(2 * np.pi * f * t + phi0)


# 不同相位的Chirp信号
phi0_list = [0, np.pi/2, np.pi, 3*np.pi/2]
signals = [chirp_signal(t, f0, f1, phi0) for phi0 in phi0_list]
# print(signals)

# 绘制信号
plt.figure(figsize=(10, 6))
for i, signal in enumerate(signals):
    plt.plot(t, signal, label=f'phi0 = {phi0_list[i]}')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Chirp Signals with Different Phases')
plt.show()

# 四帧相移法计算相位
I0 = signals[0]
I1 = signals[1]
I2 = signals[2]
I3 = signals[3]

phi_wrapped = np.arctan2(I3 - I1, I0 - I2)

# 绘制缠绕相位
plt.figure(figsize=(10, 6))
plt.plot(t, phi_wrapped, label='Wrapped Phase')
plt.xlabel('Time [s]')
plt.ylabel('Phase [rad]')
plt.legend()
plt.title('Wrapped Phase')
plt.show()

# 解缠绕相位
phi_unwrapped = np.unwrap(phi_wrapped)

# 绘制解缠绕相位
plt.figure(figsize=(10, 6))
plt.plot(t, phi_unwrapped, label='Unwrapped Phase')
plt.xlabel('Time [s]')
plt.ylabel('Phase [rad]')
plt.legend()
plt.title('Unwrapped Phase')
plt.show()

# 构建设计矩阵 X 和观测值向量 y
X = np.column_stack((t**2, t, np.ones_like(t)))  # 设计矩阵
y = phi_unwrapped  # 观测值向量

# 正规方程求解
XT_X = np.dot(X.T, X)  # X^T X
XT_y = np.dot(X.T, y)  # X^T y
beta = np.linalg.inv(XT_X).dot(XT_y)  # 系数 beta = [a, b, c]

# 提取系数
a, b, c = beta

# 拟合结果
phi_fitted = a * t**2 + b * t + c

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(t, phi_unwrapped, label='Unwrapped Phase', linestyle='-', marker='o', markersize=4)
plt.plot(t, phi_fitted, label='Fitted Phase', linestyle='--')
plt.xlabel('Time [s]')
plt.ylabel('Phase [rad]')
plt.legend()
plt.title('Fitted Phase using Normal Equation')
plt.show()

print(f"Fitted coefficients: a = {a:.3f}, b = {b:.3f}, c = {c:.3f}")
