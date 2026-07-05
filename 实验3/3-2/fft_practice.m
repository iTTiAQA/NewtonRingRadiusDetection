
%% simulate a signal
clear all,  clc, close all;
Fs = 1000;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = 1500;             % Length of signal
t = (0:L-1)*T;        % Time vector
%S = 0.7*sin(2*pi*50*t) + sin(2*pi*120*t);
%S = 1+ 0.7*sin(2*pi*50*t);
S = 0.7*sin(2*pi*50*t);
%S = 0.7*exp(1i*2*pi*50*t);
%S = sin(2*pi*50*t.^2);
subplot(4,1,1)
plot(1000*t,S)
title('Signal')
xlabel('t (milliseconds)')
ylabel('X(t)')
%% fft
 
y = fft(S);                               % Compute DFT of x
m = abs(y);                               % Magnitude32
f = (0:L-1)/L*Fs;                         % Frequency vector
subplot(4,1,2)
plot(f,m)
title('Single-Sided Amplitude Spectrum of X(t')
xlabel('f (Hz)')
ylabel('|y(f)|')
%% fft revised
 
subplot(4,1,3)
f1 = (0:L/2-1)/L*Fs;
m1 = m(1:L/2);
plot(f1,m1)
%% fftshift
 
subplot(4,1,4)
n = fftshift(m);
% f1 = f - Fs/2; 
f1 = (-L/2:L/2-1)/L*Fs;      
plot(f1,n);
