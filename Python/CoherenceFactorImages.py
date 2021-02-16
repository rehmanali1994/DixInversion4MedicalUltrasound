# Importing stuff from all folders in python path
from HelperFunctions import *
import scipy.io as sio
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import sys, os, pdb

# Input and Output Files
SoS = 1540; # Switching Sound Speed [m/s]
file_in = '../MultistaticDatasets/MultistaticDataset'+str(SoS)+'.mat';
file_out = '../SavedCoherenceFactorImages/CoherenceFactor'+str(SoS)+'.mat';

# Load Full-Synthetic Aperture Dataset
data_in = loadmat_hdf5(file_in);
time = data_in['time'][0];
scat = data_in['scat'];
scat_h = hilbert(scat, axis=0);
rxAptPos = data_in['rxAptPos'];
(T, Rx, Tx) = scat.shape
x = data_in['x'][0];
z = data_in['z'][0];
C = data_in['C'];

# Points to Focus and Get Image At
num_x = 100; num_z = 600;
pitch = np.mean(np.diff(rxAptPos[:,0]));
no_elements = rxAptPos.shape[0];
xlims = np.array([-pitch*(no_elements-1)/2, pitch*(no_elements-1)/2]);
x_img = np.linspace(xlims[0], xlims[1], num_x);
zlims = np.array([2e-3, 35e-3]);
z_img = np.linspace(zlims[0], zlims[1], num_z);
[X, Y, Z] = np.meshgrid(x_img, 0, z_img);
foc_pts = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()));

# Use Certain Transmit Elements in Full-Synthetic Aperture Dataset
tx_elmts = np.arange(0,no_elements);
txAptPos = rxAptPos[tx_elmts,:];
scat_h = scat_h[:,:,tx_elmts];

# Speed of Sound (m/s) Used to do Beamforming
cmin = 1460; cmax = 1620; cstep = 2;
Nc = int(1+(cmax-cmin)/cstep);
c_bfm = np.linspace(cmin, cmax, Nc)
cf = np.zeros((z_img.size, x_img.size, Nc));

# Focused Transmit Image Reconstruction
for c_bfm_idx in np.arange(c_bfm.size):
    # Compute Coherence Factor Images
    img = multistatic_cf(time, scat_h, foc_pts, rxAptPos, txAptPos, c_bfm[c_bfm_idx]);
    cf[:,:,c_bfm_idx] = img.reshape((x_img.size, z_img.size)).T;
    print("Speed of Sound [m/s] = "+str(c_bfm[c_bfm_idx]));

# Save Results to File
data_out = {};
data_out['x'] = x;
data_out['z'] = z;
data_out['C'] = C;
data_out['x_img'] = x_img;
data_out['z_img'] = z_img;
data_out['c_bfm'] = c_bfm;
data_out['cf'] = cf;
sio.savemat(file_out, data_out);
