# Importing stuff from all folders in python path
import numpy as np
from HelperFunctions import *
import pdb

# TESTING CODE FOR FOCUS_DATA Below
import scipy.io as sio
from scipy.signal import hilbert, filtfilt
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# Load Saved CF Images
SoS = 1540; # Switching Sound Speed [m/s]
file_saved = '../SavedCoherenceFactorImages/CoherenceFactor'+str(SoS)+'.mat';

# Load Full-Synthetic Aperture Dataset
data_in = sio.loadmat(file_saved);
x = data_in['x'][0];
z = data_in['z'][0];
C = data_in['C'];
x_img = data_in['x_img'][0];
z_img = data_in['z_img'][0];
c_bfm = data_in['c_bfm'][0];
cf = data_in['cf'];

# Assemble Coherence Factor Curves for Each Depth
cf_curves = np.mean(cf, axis = 1); # Laterally Average CF

# Estimate Average Sound Speed Upto Depth
c_bfm_increment = 0.01; # Upsampling Increment for Sound Speed Estimation
c_bfm_upsamp = np.arange(c_bfm[0], c_bfm[-1]+c_bfm_increment/2, c_bfm_increment);
cf_curves_upsamp = CubicSpline(c_bfm, cf_curves, axis = 1)(c_bfm_upsamp);
c_avg = c_bfm_upsamp[np.argmax(cf_curves_upsamp, axis = 1)];

# Smoothing Regularization
reg = 1.0e8; # Regularization Value
I = np.eye(z_img.size); F = I[:-3,:]-3*I[1:-2,:]+3*I[2:-1,:]-I[3:,:];
c_avg_smoothed = np.linalg.solve(I + reg*np.dot(F.T, F), c_avg);

# Calculate Local Sound Speed
c_local = np.diff(z_img)/np.diff(z_img/c_avg_smoothed);

# Plot Average Sound Speed vs Depth
exts = (np.min(z_img)-np.mean(np.diff(z_img)), \
    np.max(z_img)+np.mean(np.diff(z_img)), \
    np.min(c_bfm_upsamp)-np.mean(np.diff(c_bfm_upsamp)), \
    np.max(c_bfm_upsamp)-np.mean(np.diff(c_bfm_upsamp)));
plt.imshow(np.flipud(cf_curves_upsamp.T), aspect = 'auto', cmap = 'cubehelix', \
    extent = exts, vmin = np.min(cf_curves), vmax = np.max(cf_curves));
plt.title('Coherence-Based Average Sound Speed Estimates');
cbar = plt.colorbar(); cbar.set_label('Coherence Factor', rotation=90);
plt.plot(z_img, c_avg, 'k*', linewidth = 2, label='Measured');
plt.plot(z_img, c_avg_smoothed, 'r', linewidth = 2, label='Smoothed');
plt.xlabel('Imaging Depth [m]'); plt.xlim((np.min(z_img),np.max(z_img)))
plt.ylabel('Average Sound Speed [m/s]'); plt.ylim((np.min(c_bfm),np.max(c_bfm)))
plt.legend(loc='upper left'); plt.show();

# Plot Local Sound Speed vs Depth
plt.plot((z_img[:-1]+z_img[1:])/2, c_local, linewidth = 2, label='Estimated');
plt.plot(z, np.mean(C, axis=1), linewidth = 2, label='True');
plt.xlabel('Imaging Depth [m]'); plt.xlim((np.min(z_img),np.max(z_img)))
plt.ylabel('Local Sound Speed [m/s]'); plt.ylim((1460,1600))
plt.legend(loc='upper left'); plt.show();
