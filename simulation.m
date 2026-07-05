clc; clear; close all;

%% 参数设置
params.N = 512;                  % 图像尺寸
params.xRange = [-150, 150];     % x坐标范围(微米)
params.yRange = [-150, 150];     % y坐标范围(微米)
params.outerRadius = 150;        % 外圆半径(微米)
params.innerRadius = 50;         % 内圆半径(微米)
params.poreDepth = 20;           % 孔隙深度(微米)
params.n = 1.0;                  % 空气折射率
params.lambda = 0.6328;          % 光波长(微米)

%% 验证参数
assert(params.poreDepth > 0, '孔隙深度必须大于0');
aspectRatio = params.poreDepth / (params.outerRadius - params.innerRadius);
fprintf('深径比: %.2f\n', aspectRatio);

%% 创建坐标网格
[x, y] = meshgrid(linspace(params.xRange(1), params.xRange(2), params.N), ...
                  linspace(params.yRange(1), params.yRange(2), params.N));

%% 计算距离矩阵和孔隙区域
distance = sqrt(x.^2 + y.^2);
inPoreRegion = (distance <= params.outerRadius) & (distance > params.innerRadius);

%% 构建孔隙深度分布
slope = params.poreDepth / (params.outerRadius - params.innerRadius);
poreDepthMap = zeros(params.N);
poreDepthMap(inPoreRegion) = slope * (distance(inPoreRegion) - params.innerRadius);

%% 计算光程差和干涉强度
opticalPathDiff = 2 * params.n * abs(poreDepthMap) + params.lambda/2;
intensity = 0.5 * (1 + cos(2 * pi * opticalPathDiff / params.lambda));

%% 可视化结果
figure;
imshow(intensity, []);
colormap(gray);
colorbar;
title(sprintf('空心圆台孔隙等倾干涉图样\n外径:%dμm, 内径:%dμm, 深度:%dμm', ...
    params.outerRadius, params.innerRadius, params.poreDepth));
xlabel('x (微米)');
ylabel('y (微米)');

%% 显示剖面线
figure;
plot(x(params.N/2, :), intensity(params.N/2, :));
title('沿x轴中心线的强度分布');
xlabel('x (微米)');
ylabel('强度');
grid on;