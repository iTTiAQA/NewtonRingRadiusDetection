% Read the image
img = imread("figure3.png");  % Correct function name is imread, not readimage

% Convert to grayscale if needed
if size(img, 3) == 3  % Better to use size() instead of length() for images
    img = rgb2gray(img);
end

% Perform 2D FFT
newton_rings = double(img);  % Convert to double for FFT

% 方法比较
fft_rows = fft(newton_rings,[],1); % 对每列做FFT
fft_cols = fft(newton_rings,[],2); % 对每行做FFT
fft2_result = fft2(newton_rings);

% 显示结果
figure;
subplot(2,2,1); imshow(newton_rings,[]); title('原始图像');
subplot(2,2,2); imshow(log(abs(fftshift(fft_rows))+1),[]); title('fft(,[],1)');
subplot(2,2,3); imshow(log(abs(fftshift(fft_cols))+1),[]); title('fft(,[],2)');
subplot(2,2,4); imshow(log(abs(fftshift(fft2_result))+1),[]); title('fft2');