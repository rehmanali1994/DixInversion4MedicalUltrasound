import numpy as np
from scipy import linalg
from scipy.interpolate import RectBivariateSpline, interpn

def calc_times(foci, elempos, speed_of_sound):
    ''' foc_times = calc_times(foci, elempos, speed_of_sound)

    calc_times - computes focusing times

    The function computes the (Tx or Rx) time of arrival for specified focal points
    given the array element positions.

    NOTE: Primarily intended when Tx and Rx apertures are the same (i.e. no full synthetic aperture)

    INPUTS:
    foci              - M x 3 matrix with position of focal/image points of interest [m]
    elempos           - N x 3 matrix with element positions [m]
    speed_of_sound    - speed of sounds [m/s]

    OUTPUT:
    foc_times         - M x N matrix with travel times between each image point and array element '''

    foci_tmp = np.tile(foci[:,np.newaxis,:], (1,elempos.shape[0],1));
    elempos_tmp = np.tile(elempos[np.newaxis,:,:], (foci.shape[0],1,1));
    distance = np.sqrt(np.sum((foci_tmp - elempos_tmp)**2, axis = 2));
    foc_times = distance/speed_of_sound;

    return foc_times;

def multistatic_cf(t, signal, foc_pts, rxAptPos, txAptPos, speed_of_sound):
    ''' cf_img = multistatic_cf(t, signal, foc_pts, rxAptPos, txAptPos, speed_of_sound)

    multistatic_cf - Coherence Factor (CF) Beamforming of Multistatic Focused RF Data

    The function interpolates the RF signals collected using the full synthetic sequence
    to focus the data at desired locations.

    INPUTS:
    t                  - T x 1 time vector for samples of the input signal [s]
    signal             - T x N x M matrix containing input RF data to be interpolated
    foc_pts            - P x 3 matrix with position of focal points [m]
    rxAptPos           - N x 3 matrix with positions of the Rx elements [m]
    txAptPos           - M x 3 matrix with positions of the Tx elements [m]
    speed_of_sound     - speed of sounds [m/s]

    OUTPUT:
    cf_img             - vector with dimension P for CF image '''

    # time from the focus to receive  apertures (array elements)
    rx_times = calc_times(foc_pts, rxAptPos, speed_of_sound = speed_of_sound);

    # time from the transmit apertures (array elements) to focus
    tx_times = calc_times(foc_pts, txAptPos, speed_of_sound = speed_of_sound);

    # compute coherent and incoherent focused images
    coherent_img = np.zeros(foc_pts.shape[0]).astype('complex128');
    incoherent_img = np.zeros(foc_pts.shape[0]);
    for i in np.arange(rx_times.shape[1]):
        # complex image for single receive element
        rx_img = np.zeros(foc_pts.shape[0]).astype('complex128');
        for j in np.arange(tx_times.shape[1]):
            rx_img += np.interp(rx_times[:,i]+tx_times[:,j], t, signal[:,i,j], left=0, right=0);
        # Compute Coherent and Incoherent Sums
        coherent_img += rx_img; incoherent_img += np.abs(rx_img)**2;

    # compute coherence factor images
    cf_img = (np.abs(coherent_img)**2)/(incoherent_img*rx_times.shape[1]);
    return cf_img;

# Define Loadmat Function for HDF5 Format ('-v7.3 in MATLAB')
import h5py
def loadmat_hdf5(filename):
    file = h5py.File(filename,'r');
    out_dict = {}
    for key in file.keys():
        out_dict[key] = np.ndarray.transpose(np.array(file[key]));
    file.close();
    return out_dict;
