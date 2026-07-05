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
R = 2 * pi * dx / (lamda * coe(2));
x0 = -coe(3) / (2 * coe(2));
y0 = -coe(5) / (2 * coe(2));

disp('R, x0, y0')
disp([R, x0, y0])