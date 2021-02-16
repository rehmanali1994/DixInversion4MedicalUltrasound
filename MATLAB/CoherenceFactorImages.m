clear
clc

% Input and Output Files
SoS = 1570; % Switching Sound Speed [m/s]
file_in = ['../MultistaticDatasets/MultistaticDataset',num2str(SoS),'.mat'];
file_out = ['../SavedCoherenceFactorImages/CoherenceFactor',num2str(SoS),'.mat'];

% Load Full-Synthetic Aperture Dataset
load(file_in);
scat_h = hilbert(scat);
[T, Rx, Tx] = size(scat);

% Points to Focus and Get Image At
num_x = 100; num_z = 600;
pitch = mean(diff(rxAptPos(:,1)));
no_elements = size(rxAptPos,1);
xlims = [-pitch*(no_elements-1)/2, pitch*(no_elements-1)/2];
x_img = linspace(xlims(1), xlims(2), num_x);
zlims = [2e-3, 35e-3];
z_img = linspace(zlims(1), zlims(2), num_z);
[X, Y, Z] = meshgrid(x_img, 0, z_img);
foc_pts = [X(:),Y(:),Z(:)];

% Use Certain Transmit Elements in Full-Synthetic Aperture Dataset
tx_elmts = 1:no_elements;
txAptPos = rxAptPos(tx_elmts,:);
scat_h = scat_h(:,:,tx_elmts);

% Speed of Sound (m/s) Used to do Beamforming
cmin = 1460; cmax = 1620; cstep = 2;
Nc = round(1+(cmax-cmin)/cstep);
c_bfm = linspace(cmin, cmax, Nc);
cf = zeros([numel(z_img), numel(x_img), Nc]);

% Focused Transmit Image Reconstruction
for c_bfm_idx = 1:numel(c_bfm)
    % Compute Coherence Factor Images
    img = multistatic_cf(time, scat_h, foc_pts, ...
        rxAptPos, txAptPos, c_bfm(c_bfm_idx));
    cf(:,:,c_bfm_idx) = reshape(img, [numel(x_img), numel(z_img)])';
    disp(['Speed of Sound [m/s] = ', ...
        num2str(c_bfm(c_bfm_idx))]); pause(0.1);
end

% Save Results to File
save(file_out,'x','z','C','x_img','z_img','c_bfm','cf');