from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.io import savemat
import numpy as np
import cv2


def get_threshold_and_process(img):
    canny = cv2.Canny(img, threshold1=20, threshold2=30)
    # cv2.imshow("canny", canny)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canny


def read_and_process_image(input_path, threshold_value=None):
    input_image = cv2.imread(input_path)
    grey = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    if not threshold_value:
        # 应用高斯滤波去除噪声
        blurred = cv2.GaussianBlur(grey, (5, 5), 0)
        binary_image = get_threshold_and_process(blurred)
    else:
        # 二值化
        _, binary_image = cv2.threshold(grey, threshold_value, 255, cv2.THRESH_BINARY_INV)
    # 使用霍夫圆变换检测圆形
    found_circles = cv2.HoughCircles(binary_image, cv2.HOUGH_GRADIENT, dp=1, minDist=1,
                                     param1=50, param2=400, minRadius=0, maxRadius=0)

    # 如果检测到圆形，则绘制圆形
    if found_circles is not None:
        found_circles = np.round(found_circles[0, :]).astype("int")
        print(f"total {len(found_circles)} circles")
        for (x, y, r) in found_circles:
            cv2.circle(input_image, (x, y), r, (0, 255, 0), 2)
            cv2.circle(input_image, (x, y), 2, (0, 0, 255), 3)  # 绘制圆心

    cv2.imshow("input image", input_image)
    cv2.imshow("binary", binary_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return grey, found_circles


def interpolation_analyse(signal, fs, x0, if_save=False):
    T = len(radius)/fs
    t = np.linspace(0, T, len(radius), endpoint=False)  # 时间向量
    signal = np.array(signal)

    # 插值法
    # 时间变换
    t2 = (x0 - t) ** 2

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
    freq_data = np.fft.fftshift(freq_data)
    trans_freq_data = np.fft.fft(signal_trans)
    trans_freq_data = np.fft.fftshift(trans_freq_data)

    # 频率轴
    distance = T * max(t2) / (fs * max(t) ** 2)
    freq = np.fft.fftfreq(len(t), d=1 / fs)
    freq = np.fft.fftshift(freq)
    trans_freq = np.fft.fftfreq(len(t2), d=distance)
    trans_freq = np.fft.fftshift(trans_freq)

    """
    # 保留0附近的频率
    max_index = np.argmax(np.abs(trans_freq_data))
    solved_freq = abs(trans_freq[max_index])
    """
    # 忽略 0 频率附近的区间
    threshold = 1 / (50 * T)                # 忽略频率绝对值小于 threshold Hz 的数据
    print(f"ignore frequency under {threshold: .3e} pixel^(-2)")

    mask = np.abs(trans_freq) > threshold   # 创建一个掩码，排除 0 频率附近的数据
    # 在排除 0 频率附近的数据后，找到最大幅值频率
    max_index = np.argmax(np.abs(trans_freq_data[mask]))
    solved_freq = abs(trans_freq[mask][max_index])

    mdic = {
        "t": t,
        "signal": signal,
        "t2": t2,
        "signal_trans": signal_trans,
        "freq": freq,
        "freq_data": np.abs(freq_data),
        "trans_freq": trans_freq,
        "trans_freq_data": np.abs(trans_freq_data),
        "solved_freq": solved_freq
        }

    if if_save:
        # 保存数据到 .mat 文件
        savemat("interpolation_results.mat", mdic)
        print("MATLAB 数据已保存到 interpolation_results.mat")

    return mdic


def plot_sig(mdic):
    t = mdic['t']
    signal = mdic['signal']
    t2 = mdic['t2']
    signal_trans = mdic['signal_trans']
    freq = mdic['freq']
    freq_data = mdic['freq_data']
    trans_freq = mdic['trans_freq']
    trans_freq_data = mdic['trans_freq_data']

    # Plot the time-domain chirp signal
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    plt.plot(t, signal, linewidth=1)
    plt.title("Time-Domain Chirp Signal")
    plt.xlabel("Time [pixel]")
    plt.ylabel("Amplitude")

    # Plot the time-domain signal
    plt.subplot(2, 2, 2)
    plt.plot(t2, signal_trans, linewidth=1)
    plt.title("Time-Domain Transformed Signal")
    plt.xlabel("Time [pixel^2]")
    plt.ylabel("Amplitude")

    plt.subplot(2, 2, 3)
    # plt.scatter(freq, np.abs(freq_data), s=1)
    plt.plot(freq, np.abs(freq_data), linewidth=1)
    plt.title("Frequency-Domain Chirp Signal (Magnitude)")
    plt.xlabel("Frequency [1/pixel]")
    plt.ylabel("Magnitude")
    # plt.xlim(0, fs/2)  # Show only positive frequencies

    plt.subplot(2, 2, 4)
    # plt.scatter(trans_freq, np.abs(trans_freq_data), s=1)
    plt.plot(trans_freq, np.abs(trans_freq_data), linewidth=1)
    plt.title("Frequency-Domain Signal (Magnitude)")
    plt.xlabel("Frequency [1/pixel^2]")
    plt.ylabel("Magnitude")
    # plt.xlim(0, fs/2)  # Show only positive frequencies

    plt.tight_layout()
    plt.show()


def get_line_signal(sig_image, A, B, x, y):
    A, B = A/np.sqrt(A**2 + B**2), B/np.sqrt(A**2 + B**2)
    signal = []
    i = 0
    while 0 < int(A*i+x) < sig_image.shape[1] and 0 < int(B*i+y) < sig_image.shape[0]:
        try:
            signal.append(sig_image[int(B*i+y), int(A*i+x)])
        except IndexError:
            print(f"Error cord: {int(B*i+y), int(A*i+x)}")
        i += 1
    signal -= np.mean(signal)

    return signal


if __name__ == "__main__":
    fs = 1          # 1 / pixel
    dx = 1.3612     # um / pixel
    # dx = 1.294
    lamda = 0.635   # um
    # lamda = 0.5893

    # 看情况是否使用手动阈值
    threshold = 80

    # image, circles = read_and_process_image("./ring_850.jpg")
    image, circles = read_and_process_image("./figure3.png", threshold_value=threshold)
    mean_x = np.mean(circles[:, 0])  # 平均 x 坐标
    mean_y = np.mean(circles[:, 1])  # 平均 y 坐标
    print(f"shape: {image.shape}")
    print(f"circle:{mean_x, mean_y}")

    k = 100
    outputs = []
    R_lst = []
    for sigma in range(k):
        print(f"\nThis is No.{sigma + 1}/{k} solve")
        theta = sigma * 2 * np.pi / k
        radius = get_line_signal(image, np.cos(theta), np.sin(theta), mean_x, mean_y)
        print("ring signal ready")

        output = interpolation_analyse(radius, fs=fs, x0=0, if_save=False)
        print(f"frequent: {output['solved_freq']: .3e} pixel^(-2)")

        freq = output['solved_freq']    # pixel^(-2)
        R = dx**2 / (freq * lamda)      # um
        print(f"solved R: {R: .3e} um")

        outputs.append(output)
        R_lst.append(R)

    print("\nStandard R: 10.02e3")
    print(f"Final R = {np.mean(R_lst):.3e}")
    print(f"Error = {abs(np.mean(R_lst) - 10.02e3) / 10.02e3 * 100 :.2f}%")
    x = [i for i in range(len(R_lst))]
    plt.scatter(x, R_lst)
    plt.show()

    if outputs:
        plot_sig(outputs[0])

    cv2.waitKey(0)
    cv2.destroyAllWindows()
