clear;
clc;
close all;

%% 图像处理
% 参数设置
IMAGE_PATH = "figure3.png";
crop_rate_lb = 1/2;
crop_rate_rt = 1/4;

% Read the image
img = imread(IMAGE_PATH);  % Correct function name is imread, not readimage

% Convert to grayscale if needed
if size(img, 3) == 3  % Better to use size() instead of length() for images
    img = rgb2gray(img);
end

% 裁剪图像
[rows, cols] = size(img);

% 计算裁剪边界（确保不越界）
left_crop = round(cols * crop_rate_lb);     % 左侧裁剪 50%
right_crop = round(cols * (1 - crop_rate_rt)); % 保留到右侧 75%
top_crop = round(rows * crop_rate_rt);      % 上方裁剪 25%
bottom_crop = round(rows * (1 - crop_rate_lb)); % 保留到下方 50%

% 直接裁剪（注意索引范围）
cropped_img = img(top_crop+1:bottom_crop, left_crop+1:right_crop);

% 显示结果
figure;
subplot(1, 2, 1); imshow(img); title('原图');
subplot(1, 2, 2); imshow(cropped_img); title('裁剪左侧和下方 1/4');

%% 傅里叶变换
% Perform 2D FFT
I = double(cropped_img);  % Convert to double for FFT
F = fft2(I);  % Correct way to compute 2D FFT
F_shifted = fftshift(F);  % Center the frequency components
magnitude = log(abs(F_shifted) + 1);  % Logarithmic scale for better visualization

% Display results
figure;
subplot(1,2,1);
imshow(img, []);  % Show original image
title('Original Image');

subplot(1,2,2);
% imshow(magnitude, []);  % Show FFT magnitude spectrum
[M, N] = size(magnitude);
[u, v] = meshgrid((-N/2:N/2-1)/N, (-M/2:M/2-1)/M);
surf(u, v, magnitude, 'EdgeColor', 'none');
colorbar;
title('FFT Magnitude Spectrum');

%% 重建信号
% 从频域重建图像
% F_reconstructed = ifftshift(F_shifted);  % 先将频谱移回原始位置
% I_reconstructed = real(ifft2(F_reconstructed));  % 逆傅里叶变换并取实部

% 显示重建结果
% figure;
% imshow(uint8(I_reconstructed));
% title('Reconstructed Image');

%% 滤波截取cos
% 截取左上角（低频部分）
[M, N] = size(F_shifted);

% 补零至原始尺寸
filtered_F = zeros(M, N);
filtered_F(end-floor(M/2):end, 1:floor(N/2)) = F(end-floor(M/2):end, 1:floor(N/2));
% filtered_F(1:floor(M/2), end-floor(N/2):end) = F(1:floor(M/2), end-floor(N/2):end);

% 逆变换（由于对称性被破坏，结果仍有虚部）
Ip = ifft2(filtered_F);
% Ip = ifft2(F);

% 反移位后逆变换
% filtered_F = ifftshift(filtered_F_shifted);
% Ip = real(ifft2(filtered_F));  % 取实部消除数值误差虚部

% 显示结果
figure;
subplot(1,2,1); 
imshow(log(1 + abs(filtered_F)), [3 10]); title('筛选频谱');
subplot(1,2,2); 
imshow(abs(Ip), []); title('滤波重建');

%% 解包相位
tan_theta = imag(Ip) ./ real(Ip);
tan_theta(isnan(tan_theta)) = 0;
figure;
% surf(tan_theta, 'EdgeColor', 'none')
imshow(tan_theta, [-20, 20]); colorbar;
title('tan theta');

% figure;
% % surf(tan_theta, 'EdgeColor', 'none')
% imshow(real(Ip), [-20, 20]); colorbar;
% title('cos theta');
% 
% figure;
% % surf(tan_theta, 'EdgeColor', 'none')
% imshow(real(imag(Ip)), [-20, 20]); colorbar;
% title('sin theta');

phi = cunwrap(tan_theta);

figure;
% subplot(2, 2, 1);
% surf(tan_theta, 'EdgeColor', 'none');
% title("tanTheta");
% colorbar;

subplot(1, 2, 1);
surf(phi, 'EdgeColor', 'none');
title("phi");
colorbar;

subplot(1, 2, 2);
imshow(phi, []);
title("phi");

% 保存为 JPEG 格式
% imwrite(phi, 'unwrap.jpg');  

%% 回归计算
% 定义矩阵大小
[m, n] = size(phi);  % 假设是 m×n 矩阵

% 生成网格坐标
[X, Y] = meshgrid(1:n, 1:m);

% 假设 x 和 y 是列向量
x = X(:);  % 确保 x 是列向量
y = Y(:);  % 确保 y 是列向量

% 构造矩阵，每行是 [x^2, x, y^2, y]
DataMatrix = [x.^2, x, y.^2, y];

% 添加偏置项（第一列全为 1）
DataMatrix = [ones(size(DataMatrix,1),1), DataMatrix];

% 从 phi 矩阵中提取对应的值
phiData = phi(:);  % 将 phi 矩阵展平为列向量

% 检查维度是否匹配
if size(DataMatrix, 1) ~= size(phiData, 1)
    error('DataMatrix 和 phiData 的行数不匹配');
end

% 计算回归系数
coe = (DataMatrix' * DataMatrix) \ (DataMatrix' * phiData);

% 显示回归系数
disp('回归系数:');
disp(coe');

lamda = 0.635;      % um
dx = 1.3612;        % um/pixel
lamda = lamda / dx; % pixel
R = 2 * 2 * pi * dx / (lamda * coe(2)); % um
x0 = -coe(3) / (2 * coe(2));        % pixel
y0 = -coe(5) / (2 * coe(2));        % pixel
error = abs(R - 10.02e3) / 10.02e3 * 100;
disp('R, x0, y0')
disp([R, x0, y0])
fprintf("\nerror: %.2f%%\n", error);