import numpy as np
from matplotlib import pyplot as plt


def is_monotonic(lst):
    increasing = True
    decreasing = True

    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            increasing = False
        if lst[i] > lst[i - 1]:
            decreasing = False

    if increasing:
        return "单调递增"
    elif decreasing:
        return "单调递减"
    else:
        return "不是单调的"


def test():
    # 参数
    T = 2.0  # 总时间
    fs = 100  # 采样频率
    t = np.linspace(0, T, int(T * fs), endpoint=False)  # 时间向量

    # 生成信号
    signal = np.cos(8 * np.pi * t)

    zero = False
    i = 1
    while True:
        if zero:
            for j in range(int(np.sqrt(i))):
                if i + j >= len(signal):
                    break
                signal[i+j] = 0
            zero = False
        else:
            zero = True
        i += int(np.sqrt(i))
        if i >= len(signal):
            break

    # 计算傅里叶变换
    # freq_data = np.fft.fft(signal)
    freq_data = np.fft.fftshift(np.fft.fft(signal))

    # 频率轴
    # freq = np.fft.fftfreq(len(t), d=1/fs)
    freq = np.fft.fftshift(np.fft.fftfreq(len(t), d=1 / fs))

    max_index = np.argmax(np.abs(freq_data))
    solved_freq = abs(freq[max_index])

    print(f"频率为：{solved_freq: .2f} Hz")

    # Plot the time-domain chirp signal
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, signal)
    plt.title("Time-Domain Signal")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")

    plt.subplot(2, 1, 2)
    # plt.scatter(freq, np.abs(freq_data), s=1)
    plt.plot(freq, np.abs(freq_data), linewidth=1)
    plt.title("Frequency-Domain Signal (Magnitude)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    # plt.xlim(0, fs/2)  # Show only positive frequencies

    plt.tight_layout()
    plt.show()

test()

if __name__ == "__main__":
    print("choose a method: interpolation, zero_padding, maintain")
    _input = str(input(":"))
    if _input == "interpolation":
        from interpolation import *
    elif _input == "zero_padding":
        from zero_padding import *
    elif _input == "maintain":
        from maintain import *
