The first stage of sound speed estimation is to create a stack of coherence factor images focused at various sound speeds.

For each simulation, [DixInversion4MedicalUltrasound
/MATLAB/CoherenceFactorImages.m](DixInversion4MedicalUltrasound
/MATLAB/CoherenceFactorImages.m) and [DixInversion4MedicalUltrasound
/Python/CoherenceFactorImages.py](DixInversion4MedicalUltrasound
/Python/CoherenceFactorImages.py) computes this stack of coherence factor images and saves them here as .mat files.

These .mat files are read in [DixInversion4MedicalUltrasound
/MATLAB/CoherenceFactorImages.m](DixInversion4MedicalUltrasound
/MATLAB/SoundSpeedEstimation.m) and [DixInversion4MedicalUltrasound
/Python/CoherenceFactorImages.py](DixInversion4MedicalUltrasound
/Python/SoundSpeedEstimation.py) where sound speed is estimated as a function of depth.
