% Script to test functionality of findBeamwidth.m
%
% Generates a sample pattern (sin(phi/2))^2 for phi in [0,359], adds noise,
% and plots the clean and noisy pattern in decibels. The beamwidth
% (with parameters passed to findBeamwidth.m set below) is calculated and
% drawn on the noisy data graph. This is then repeated for the same pattern
% rotated 120 degrees (with a fresh set of noise added to the clean data).
% 
% Written by Brian Gibbons
% October 10, 2013

% Parameters - play around with these to adjust settings
angleCount = 720;
noise_level = -10;  % [dBm] power of noise
beamWidthDepth = 3; % [dB] how much edges of the beam differ from the max
averagingWindowSize = 4; % See documentation of findBeamwidth


angles = linspace(0,359,angleCount);  % Measurement angles

data = sind(angles/2).^2;   % Simulated measurement
data_noisy = data + wgn(1,angleCount,noise_level,'dBm');  % Add noise to the data
data_noisy = data_noisy - min(data_noisy);  % Remove negative values

data_shifted = circshift(data',floor(angleCount/3))';   % Shift peak location
data_shifted_noisy = data_shifted + wgn(1,angleCount,noise_level,'dBm');
data_shifted_noisy = data_shifted_noisy - min(data_shifted_noisy);

% Convert to dB
data_dB = 10*log10(data);
data_dB = data_dB - max(data_dB); % Normalize to 0dB

data_noisy_dB = 10*log10(data_noisy);
data_noisy_dB = data_noisy_dB - max(data_noisy_dB);

data_shifted_dB = 10*log10(data_shifted);
data_shifted_dB = data_shifted_dB - max(data_shifted_dB);

data_shifted_noisy_dB = 10*log10(data_shifted_noisy);
data_shifted_noisy_dB = data_shifted_noisy_dB - max(data_shifted_noisy_dB);


% % Linear Plots
% plot(angles, data);
% axis([0 360 0 1]);
% set(gca, 'XTick', 0:45:360);
% grid on;
% title('data');
% xlabel('Angle [\circ]');
% ylabel('Pattern [linear]');
% 
% figure;
% plot(angles, data_noisy);
% axis([0 360 0 max(data_noisy)]);
% set(gca, 'XTick', 0:45:360);
% grid on;
% title('data noisy');
% xlabel('Angle [\circ]');
% ylabel('Pattern [linear]');
% 
% figure;
% plot(angles, data_shifted);
% axis([0 360 0 1]);
% set(gca, 'XTick', 0:45:360);
% grid on;
% title('data shifted');
% xlabel('Angle [\circ]');
% ylabel('Pattern [linear]');
% 
% figure;
% plot(angles, data_noisy_shifted);
% axis([0 360 0 max(data_noisy_shifted)]);
% set(gca, 'XTick', 0:45:360);
% grid on;
% title('data noisy shifted');
% xlabel('Angle [\circ]');
% ylabel('Pattern [linear]');

% dB Plots
plot(angles, data_dB);
axis([0 360 -60 0]);
set(gca, 'XTick', 0:45:360);
set(gca, 'YTick', -60:3:0);
grid on;
title('clean, unshifted data');
xlabel('Angle [\circ]');
ylabel('Pattern [dB]');

figure;
plot(angles, data_noisy_dB);
axis([0 360 -60 0]);
set(gca, 'XTick', 0:45:360);
set(gca, 'YTick', -60:3:0);
grid on;
title('noisy, unshifted data');
xlabel('Angle [\circ]');
ylabel('Pattern [dB]');
hold on;
[beamwidth, top, bot, beammax] = findBeamwidth(beamWidthDepth, ...
                                    data_noisy_dB, averagingWindowSize);
disp(' ');
disp('Index results for unshifted noisy data:');
str = sprintf('Beamwidth = %.1f degrees\nBottom (left) beam edge = %.1f degrees', ...
                beamwidth*(360/angleCount), angles(bot));
disp(str);
str = sprintf('Top (right) beam edge = %.1f degrees\nBeam maximum = %.1f degrees', ...
                angles(top), angles(beammax));
disp(str);
plot(angles(beammax), data_noisy_dB(beammax), 'go');
plot(angles(top), data_noisy_dB(top), 'r<');
plot(angles(bot), data_noisy_dB(bot), 'r>');
hold off;

figure;
plot(angles, data_shifted_dB);
axis([0 360 -60 0]);
set(gca, 'XTick', 0:45:360);
set(gca, 'YTick', -60:3:0);
grid on;
title('clean, shifted data');
xlabel('Angle [\circ]');
ylabel('Pattern [dB]');

figure;
plot(angles, data_shifted_noisy_dB);
axis([0 360 -60 0]);
set(gca, 'XTick', 0:45:360);
set(gca, 'YTick', -60:3:0);
grid on;
title('noisy, shifted data');
xlabel('Angle [\circ]');
ylabel('Pattern [dB]');
hold on;
[beamwidth, top, bot, beammax] = findBeamwidth(beamWidthDepth, ...
                                data_shifted_noisy_dB, averagingWindowSize);
disp(' ');
disp('Index results for shifted noisy data:');
str = sprintf('Beamwidth = %.1f degrees\nBottom (left) beam edge = %.1f degrees', ...
                beamwidth*(360/angleCount), angles(bot));
disp(str);
str = sprintf('Top (right) beam edge = %.1f degrees\nBeam maximum = %.1f degrees', ...
                angles(top), angles(beammax));
disp(str);
plot(angles(beammax), data_shifted_noisy_dB(beammax), 'go');
plot(angles(top), data_shifted_noisy_dB(top), 'r<');
plot(angles(bot), data_shifted_noisy_dB(bot), 'r>');
hold off;
