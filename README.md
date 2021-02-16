# DixInversion4MedicalUltrasound

Sound Speed Estimator for Layered Media in Medical Ultrasound Imaging. 

Medical ultrasound imaging typically assumes a constant sound speed of 1540 m/s in the medium. However, sound speed is known to vary by tissue type (e.g. muscle, connective tissues, fat). The reconstruction of sound speed in the human body using backscattered ultrasound signals is regarded as an inverse problem. 

We provide sample data and algorithms presented in

> Ali, R.; Telichko, A.; Wang, H.; Sukumar, U.; Vilches-Moure, J.; Paulmurugan, R.; Dahl, J. "Local Sound Speed Estimation for Pulse-Echo Ultrasound in Layered Media". *Manuscript submitted for publication.*

for the reconstruction of sound speed in heterogeneous and diffuse-scattering medium when sound speed varies as a function of depth into the medium. We follow an approach reminiscent of Dix inversion from seismic imaging (hence the name DixInversion4MedicalUltrasound).

If you use the code/algorithm for research, please cite the above paper. 

You can reference a static version of this code by its DOI number:
INSERT DOI HERE

# Code and Sample Datasets
The sound speed reconstruction algorithm is implemented in both MATLAB and Python. The algorithm is broken into two steps. The first step is to create a stack of coherence factor images focused at various sound speeds (implemented in [MATLAB/CoherenceFactorImages.m](MATLAB/CoherenceFactorImages.m) and [Python/CoherenceFactorImages.py](Python/CoherenceFactorImages.py)). These coherence factor image stacks are saved in [SavedCoherenceFactorImages](SavedCoherenceFactorImages) as .mat files. The second step is to estimate the average and local sound speed as a function of depth from this stack of coherence images (implemented in [MATLAB/SoundSpeedEstimation.m](MATLAB/SoundSpeedEstimation.m) and [Python/CoherenceFactorImages.py](Python/SoundSpeedEstimation.py))

**Please download the sample data (.mat files) under the [releases](https://github.com/rehmanali1994/DixInversion4MedicalUltrasound/releases) tab for this repository, and place that data in [MultistaticDatasets](MultistaticDatasets).**

# Sample results
