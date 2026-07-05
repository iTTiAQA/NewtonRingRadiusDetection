%unwrap_experiment
close all, clear all, clc;
phai = 0: (0.00001*2*pi): 2*pi;
x = 1: length(phai);
y = tan(phai);
% y = cos(phai);
phair = atan(y);

subplot(3,1,1);
plot(x, phai, x, phair, 'Linewidth',3);
phairr = unwrap(2*phair)/2;     
% phairr = unwrap(phair,1);
subplot(3,1,2);
plot(x, phair,'Linewidth',3);
title('atan')
subplot(3,1,3);
plot(x, phairr,'Linewidth',3);
title('unwrap of atan')