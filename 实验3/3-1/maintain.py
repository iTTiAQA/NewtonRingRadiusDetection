import numpy as np
from matplotlib import pyplot as plt

# 参数
T = 2.0     # 总时间
fs = 100    # 采样频率
x0 = 0.5      # 偏移量
t = np.linspace(0, T, int(T * fs), endpoint=False)  # 时间向量


# 定义 Chirp 信号
def get_1D_chirp(x, phi):
    return 10 * np.cos(9 * np.pi * (x - x0)**2 + phi)


# 生成 Chirp 信号
signal = get_1D_chirp(t, 0.5 * np.pi)

# 保持方法
signal_trans = [np.NaN for _ in range(int(max((len(signal) - x0 * fs)**2, (x0 * fs)**2)))]
for i, sig in enumerate(signal):
    signal_trans[int((i - x0 * fs)**2)] = sig
temp = 0
for i, sig in enumerate(signal_trans):
    if np.isnan(sig):
        signal_trans[i] = temp
    else:
        temp = sig

t2 = [i / fs**2 for i in range(len(signal_trans))]

# 计算信号的傅里叶变换
freq_data = np.fft.fft(signal)
trans_freq_data = np.fft.fft(signal_trans)
# print(trans_freq_data)

# 频率轴
freq = np.fft.fftfreq(len(t), d=1/fs)
trans_freq = np.fft.fftfreq(len(t2), d=1/fs**2)
# 忽略 0 频率附近的区间
threshold = 0.5                         # 忽略频率绝对值小于 0.5 Hz 的数据
mask = np.abs(trans_freq) > threshold   # 创建一个掩码，排除 0 频率附近的数据

# 在排除 0 频率附近的数据后，找到最大幅值频率
max_index = np.argmax(np.abs(trans_freq_data[mask]))
solved_freq = abs(trans_freq[mask][max_index])

print(f"频率为：{solved_freq: .2f} Hz")

# Plot the time-domain chirp signal
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(t, signal, linewidth=1)
plt.title("Time-Domain Chirp Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")


# Plot the time-domain signal
plt.subplot(2, 2, 2)
plt.plot(t2, signal_trans, linewidth=1)
plt.title("Time-Domain Transformed Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")


plt.subplot(2, 2, 3)
# plt.scatter(freq, np.abs(freq_data), s=1)
plt.plot(freq, np.abs(freq_data), linewidth=1)
plt.title("Frequency-Domain Chirp Signal (Magnitude)")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
# plt.xlim(0, fs/2)  # Show only positive frequencies

plt.subplot(2, 2, 4)
# plt.scatter(trans_freq, np.abs(trans_freq_data), s=1)
plt.plot(trans_freq, np.abs(trans_freq_data), linewidth=1)
plt.title("Frequency-Domain Signal (Magnitude)")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
# plt.xlim(0, fs/2)  # Show only positive frequencies

plt.tight_layout()
plt.show()
