close all;

% %% 参数设置
% fs = 1000;          % 采样频率 (Hz)
% T = 10;              % 信号持续时间 (s)
% t = 0:1/fs:T-1/fs;  % 时间向量
% N = length(t);      % 信号长度
% 
% f0 = 1;            % 起始频率 (Hz)
% f1 = 10;           % 结束频率 (Hz)
% 

% 参数
T = 9;     % 总时间
fs = 1000;    % 采样频率
x0 = 0;    % 偏移量
t = linspace(0, T, T * fs);  % 时间向量（MATLAB的linspace默认包含端点）
N = length(t);      % 信号长度

%% 生成chirp信号
% chirp_signal = chirp(t, f0, T, f1, 'linear');
chirp_signal = get_1D_chirp(t, x0, 0);

%% 绘制时域信号
figure;
subplot(2,1,1);
plot(t, chirp_signal);
xlabel('时间 (s)');
ylabel('幅度');
title('Chirp信号 (时域)');
grid on;

%% 傅里叶变换F
f = (-N/2:N/2-1)*(fs/N);  % 频率轴
F = fft(chirp_signal);
fft_result = fftshift(F);  % 进行FFT并中心化

magnitude = abs(fft_result);  % 幅度谱
phase = angle(fft_result);    % 相位谱

%% 绘制频域结果
subplot(2,1,2);
plot(f, magnitude);
xlabel('频率 (Hz)');
ylabel('幅度');
title('Chirp信号的傅里叶变换 (幅度谱)');
xlim([-150 150]);  % 限制频率显示范围
grid on;

%% 处理分析
cutoff = floor(N/2);  % 保留1/2的频谱
filtered_F = zeros(1,N);
filtered_F(cutoff:end) = 2*fft_result(cutoff:end);

% 逆傅里叶变换
Ip = ifft(ifftshift(filtered_F));  % 注意要先ifftshift
% figure;
% plot(t, abs(Ip));
% xlabel('Time [s]');
% ylabel('Magnitude');
% title('Reconstructed');
% grid on;

% 计算缠绕相位 (使用atan2)
phi_wrapped = atan2(imag(Ip), real(Ip));

% 绘制缠绕相位
% figure;
% plot(t, phi_wrapped);
% xlabel('Time [s]');
% ylabel('Phase [rad]');
% title('Wrapped Phase');
% grid on;

%% 解缠绕相位
phi_unwrapped = unwrap(phi_wrapped);

% 绘制解缠绕相位
% figure;
% plot(t, phi_unwrapped);
% xlabel('Time [s]');
% ylabel('Phase [rad]');
% title('Unwrapped Phase');
% grid on;

%% 二次函数拟合
X = [t'.^2, t', ones(length(t), 1)];  % 设计矩阵 [t^2, t, 1]
y = phi_unwrapped';  % 观测值向量

% 正规方程求解
XT_X = X' * X;      % X^T X
XT_y = X' * y;      % X^T y
beta = XT_X \ XT_y; % 使用反斜杠运算符求解线性方程组

% 提取系数
a = beta(1);
b = beta(2);
c = beta(3);

% 拟合结果
phi_fitted = a * t.^2 + b * t + c;

% 绘制结果
figure;
hold on;
plot(t, phi_unwrapped, 'o-', 'DisplayName', 'Unwrapped Phase');
plot(t, phi_fitted, '--', 'DisplayName', 'Fitted Phase');
xlabel('Time [s]');
ylabel('Phase [rad]');
legend;
title('Quadratic Fitted Phase using Normal Equation');
grid on;

fprintf("quadratic fit:\n")
fprintf('Fitted coefficients: a = %f, b = %f, c = %f\n', a, b, c);

%% 对勾函数拟合
% threshold = 10/fs;   % 等于第一个非零点
% valid_idx = t >= threshold;
% t_valid = t(valid_idx);
% phi_unwrapped_valid = phi_unwrapped(valid_idx);
% 
% % 构建设计矩阵
% X = [t_valid', 1./t_valid', ones(length(t_valid), 1)];
% y = phi_unwrapped_valid';
% 
% % 求解（添加正则化更稳定）
% lambda = 1e-6;
% XT_X = X' * X + lambda * eye(3);
% beta = XT_X \ (X' * y);
% 
% % 提取系数
% a = beta(1);  % t的系数
% c = beta(2);  % 1/t的系数
% b = beta(3);  % 常数项
% 
% % 绘制结果
% figure;
% hold on;
% plot(t_valid, phi_unwrapped_valid, 'o', 'DisplayName', 'Data');
% plot(t_valid, a*t_valid + b + c./t_valid, '-', 'DisplayName', 'Fitted');
% xlabel('Time (s)');
% ylabel('Phase (rad)');
% legend;
% title('Fractional Fitted Phase using Normal Equation');
% grid on;
% 
% fprintf("fractional fit:\n")
% fprintf('Fitted coefficients: a = %f, b = %f, c = %f\n', a, b, c);

%% 无常数项的三次函数拟合
X = [t', t'.^2, t'.^3];  % 设计矩阵 [t, t^2, t^3]（无常数项）
y = phi_unwrapped';      % 观测值向量

% 正规方程求解
XT_X = X' * X;      % X^T X
XT_y = X' * y;      % X^T y
beta = XT_X \ XT_y; % 使用反斜杠运算符求解线性方程组

% 提取系数
a1 = beta(1);  % t 的系数
a2 = beta(2);  % t^2 的系数
a3 = beta(3);  % t^3 的系数

% 拟合结果
phi_fitted = a1 * t + a2 * t.^2 + a3 * t.^3;

% 绘制结果
figure;
hold on;
plot(t, phi_unwrapped, 'o-', 'DisplayName', 'Unwrapped Phase');
plot(t, phi_fitted, '--', 'DisplayName', 'Fitted Phase');
xlabel('Time [s]');
ylabel('Phase [rad]');
legend;
title('Cubic Fitted Phase (No Constant Term) using Normal Equation');
grid on;

fprintf("cubic fit:\n");
fprintf('Fitted coefficients: a3 = %f, a2 = %f, a1 = %f\n', a3, a2, a1);

%% 定义 Chirp 信号函数
function y = get_1D_chirp(x, x0, phi)
    y = 10 * cos(9 * pi * (x - x0).^2 + phi);
end