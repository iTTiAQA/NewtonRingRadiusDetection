clear;
clc;

% 读取图像并转换为灰度图
image1 = im2single(imread('figures/1.png'));
if size(image1, 3) == 3
    image1 = rgb2gray(image1);
end
image2 = im2single(imread('figures/2.png'));
if size(image2, 3) == 3
    image2 = rgb2gray(image2);
end
image3 = im2single(imread('figures/3.png'));
if size(image3, 3) == 3
    image3 = rgb2gray(image3);
end
image4 = im2single(imread('figures/4.png'));
if size(image4, 3) == 3
    image4 = rgb2gray(image4);
end

% 打印图像尺寸
disp(size(image1));

% 计算分子和分母
numerator = double(image4 - image2);
denominator = double(image1 - image3);

% 找到矩阵的最小值和最大值
min_numerator = min(numerator(:)); % 矩阵的最小值
max_numerator = max(numerator(:)); % 矩阵的最大值
min_denominator = min(denominator(:)); % 矩阵的最小值
max_denominator = max(denominator(:)); % 矩阵的最大值

% 线性变换到 [-1, 1]
numerator_normalized = 2 * (numerator - min_numerator) / (max_numerator - min_numerator) - 1;
denominator_normalized = 2 * (denominator - min_denominator) / (max_denominator - min_denominator) - 1;

tan_theta = -numerator_normalized ./ denominator_normalized;
% 去除NaN值
tan_theta(isnan(tan_theta)) = 0;

% % 计算反正切
% theta = atan(tan_theta);

% % 替换操作
% theta(theta >= 0.99*atan(inf)) = 1000;
% theta(theta <= 0.99*atan(-inf)) = 1000;
% theta(isnan(theta)) = 0;

% 相位解包裹
% 设置 options 结构体
% options = struct();
% % options.Weight = ones(size(theta));  % 权重矩阵，默认所有像素权重为 1
% options.CutSize = 1;               % 高斯核宽度
% options.RoundK = true;            % 不强制 K1/K2 为整数
% options.MaxBlockSize = inf;        % 目标块大小
% options.Overlap = 0.25;            % 块之间的重叠比例
% options.Verbose = true;            % 打印信息
% options.LPoption = optimset('Display', 'off');  % LINPROG 选项

% phi = cunwrap(theta);
phi = cunwrap(tan_theta);


subplot(2, 1, 1);
surf(tan_theta);
title("Theta",'EdgeColor', 'none');
colorbar;

subplot(2, 1, 2);
surf(phi,'EdgeColor', 'none');
title("phi");
colorbar;

% 保存为 JPEG 格式
% imwrite(phi, 'unwrap.jpg');  

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

lamda = 0.635; % um
dx = 1.3612;    % um/pixel
lamda = lamda / dx; % pixel
R = 2 * pi * dx / (lamda * coe(2)); % um
x0 = -coe(3) / (2 * coe(2));    % pixel
y0 = -coe(5) / (2 * coe(2));    % pixel

disp('R, x0, y0')
disp([R, x0, y0])