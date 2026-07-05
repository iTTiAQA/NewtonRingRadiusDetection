% 仿真一个正弦图像
close all; clc; clear

Fs = 1000;                          % Sampling frequency                    
T = 1/Fs;                           % Sampling period       
L = 1500;                           % Length of signal
t = (0:L-1)*T;                      % Time vector
% S = 0.7*sin(2*pi*50*t);

[X, Y] = meshgrid(t);               %绘制二维坐标点，X为行，Y为列
phase = 2*pi*50*X + 2*pi*100*Y;     %沿着行的频率50Hz,沿着列的频率100Hz
I = cos(phase);
figure, imshow(I,[]); 
