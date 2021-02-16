The first stage of sound speed estimation is to create a stack of coherence factor images focused at various sound speeds.

For each multistatic dataset, [MATLAB/CoherenceFactorImages.m](../MATLAB/CoherenceFactorImages.m) and [Python/CoherenceFactorImages.py](../Python/CoherenceFactorImages.py) computes this stack of coherence factor images and saves them here as .mat files.

These .mat files are read in [MATLAB/SoundSpeedEstimation.m](../MATLAB/SoundSpeedEstimation.m) and [Python/SoundSpeedEstimation.py](../Python/SoundSpeedEstimation.py) where sound speed is estimated as a function of depth.
