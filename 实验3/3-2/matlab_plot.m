% 加载数据
data = load('interpolation_results.mat');

% 绘制时域信号
figure;
subplot(2,2,1);
plot(data.t, data.signal, 'LineWidth', 1);
title('Time-Domain Chirp Signal');
xlabel('Time [s]');
ylabel('Amplitude');

subplot(2,2,2);
plot(data.t2, data.signal_trans, 'LineWidth', 1);
title('Time-Domain Transformed Signal');
xlabel('Time [s]');
ylabel('Amplitude');

% 绘制频域信号
subplot(2,2,3);
plot(data.freq, data.freq_data, 'LineWidth', 1);
title('Frequency-Domain Chirp Signal (Magnitude)');
xlabel('Frequency [Hz]');
ylabel('Magnitude');

subplot(2,2,4);
plot(data.trans_freq, data.trans_freq_data, 'LineWidth', 1);
title('Frequency-Domain Signal (Magnitude)');
xlabel('Frequency [Hz]');
ylabel('Magnitude');

% 输出解算出的频率
disp(['Solved Frequency: ', num2str(data.solved_freq)]);
