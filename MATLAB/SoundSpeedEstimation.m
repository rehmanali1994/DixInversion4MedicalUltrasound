clear
clc

% Load Saved CF Images
SoS = 1570; % Switching Sound Speed [m/s]
file_saved = ['../SavedCoherenceFactorImages/CoherenceFactor', num2str(SoS), '.mat'];

% Load Full-Synthetic Aperture Dataset
load(file_saved);

% Assemble Coherence Factor Curves for Each Depth
cf_curves = squeeze(mean(cf, 2))'; % Laterally Average CF

% Estimate Average Sound Speed Upto Depth
c_bfm_increment = 0.01; % Upsampling Increment for Sound Speed Estimation
c_bfm_upsamp = c_bfm(1):c_bfm_increment:c_bfm(end);
cf_curves_upsamp = interp1(c_bfm, cf_curves, c_bfm_upsamp);
[~,index] = max(cf_curves_upsamp); c_avg = c_bfm_upsamp(index);

% Smoothing Regularization
reg = 1.0e8; % Regularization Value
I = eye(numel(z_img)); % Identity Matrix
F = I(1:end-3,:)-3*I(2:end-2,:)+3*I(3:end-1,:)-I(4:end,:);
c_avg_smoothed = (I+reg*F'*F)\c_avg(:);

% Calculate Local Sound Speed
c_local = diff(z_img(:))./diff(z_img(:)./c_avg_smoothed(:));

% Plot Average Sound Speed vs Depth
figure; imagesc(z_img, c_bfm_upsamp, cf_curves_upsamp)
title('Coherence-Based Average Sound Speed Estimates');
cbar = colorbar; ylabel(cbar, 'Coherence Factor'); hold on;
plot(z_img, c_avg, 'k*', 'Linewidth', 2);
plot(z_img, c_avg_smoothed, 'r', 'Linewidth', 2);
xlabel('Imaging Depth [m]'); xlim([min(z_img),max(z_img)]);
ylabel('Average Sound Speed [m/s]'); ylim([min(c_bfm),max(c_bfm)]);
legend('Measured', 'Smoothed', 'Location', 'Northwest');
set(gca, 'YDir', 'normal');

% Plot Local Sound Speed vs Depth
figure; plot((z_img(2:end)+z_img(1:end-1))/2, c_local, 'Linewidth', 2);
hold on; plot(z, mean(C,2), 'Linewidth', 2);
xlabel('Imaging Depth [m]'); xlim([min(z_img),max(z_img)]);
ylabel('Local Sound Speed [m/s]'); ylim([1460,1600]);
legend('Estimated', 'True', 'Location', 'Northwest');
