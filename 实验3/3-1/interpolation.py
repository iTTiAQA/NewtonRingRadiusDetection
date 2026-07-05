import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

# 参数
T = 5.0     # 总时间
fs = 100    # 采样频率
x0 = 1      # 偏移量
t = np.linspace(0, T, int(T * fs), endpoint=False)  # 时间向量


# 定义 Chirp 信号
def get_1D_chirp(x, phi):
    return 10 * np.cos(4 * np.pi * (x - x0)**2 + phi)


# 生成 Chirp 信号
signal = get_1D_chirp(t, 0.5 * np.pi)


# 插值法
# 时间变换
t2 = (x0 - t)**2

# 移除重复的 t2 值
unique_t2, unique_indices = np.unique(t2, return_index=True)
unique_signal = signal[unique_indices]

# 插值
get_signal_trans = interp1d(unique_t2, unique_signal, kind='cubic')

# 生成新的时间向量
t2 = np.linspace(min(t2), max(t2), len(t2))
signal_trans = get_signal_trans(t2)


# 计算信号的傅里叶变换
freq_data = np.fft.fft(signal)
trans_freq_data = np.fft.fft(signal_trans)

# 频率轴
distance = T * max(t2) / (fs * max(t)**2)
freq = np.fft.fftfreq(len(t), d=1/fs)
trans_freq = np.fft.fftfreq(len(t2), d=distance)


max_index = np.argmax(np.abs(trans_freq_data))
solved_freq = abs(trans_freq[max_index])

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
