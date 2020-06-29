# Driving Simulator Validation of Machine Learning Classification for a Surface Electromyography-based Steering Assistance Interface
This repository contains scripts and data files to supplement results published in a paper for the 11th International Conference on Applied Human Factors and Ergonomics (AHFE 2020).  Link to paper: https://doi.org/10.1007/978-3-030-51064-0_19.

## Setup
### Getting Started
Install Python 3.7 and download this repository.
```
git clone https://github.com/azukipan/ml_for_semg_ahfe2020.git
```
### putEMG Dataset
1. Follow setup instructions for the putEMG dataset at https://biolab.put.poznan.pl/putemg-dataset/. 
2. Download the putEMG dataset repository from https://github.com/biolab-put/putemg-downloader.
3. Download exammple Python scripts from https://github.com/biolab-put/putemg_examples.
### BeamNG.research Driving Simulator
1. Using Windows 10 64 Bit, download BeamNG.reserach v1.4.0.0 using Subversion (https://subversion.apache.org/).
```
svn checkout https://projects.beamng.com/svn/research@14
```
2. In the directory where BeamNG.research was downloaded, open the driving simulator
```
.\research\trunk\BeamNG.research.x64.exe
```
In the simulator, go to Scenarios > Download More! > Mods and download the `simple_map.zip`. 
3. Install Python interface `beamngpy` for BeamNG.research.
```
pip install beamngpy==1.11
```
## Evaluating Machine Learning Methods
In ordr to evaluate Linear Discriminant Analysis (LDA), as published in the AHFE 2020 paper, go to the putEMG dataset directory for `putemg_examples` and run `shallow_learn.py` with Python 3.7.
```
mkdir shallow_learn_results

python shallow_learn.py ../Data-HDF5/ ./shallow_learn_results/

python shallow_learn_plot_results.py ./shallow_learn_results/
```

## Calculating sEMG Signal Processing Times
1. Processing time results have been provided in `ml_for_semg_ahfe2020/gesture_learning_results_AHFE_2020`.
2. Results are reporduced by running scripts from this repository.
```
python processing_time_wrist_extension.py 

python processing_time_wrist_flexion.py 
```

## Running Driving Simulations
1. Driving simulation trial data for target trajectories and measured trajectories are provided in `ml_for_semg_ahfe2020/results_right_u-turn` and `ml_for_semg_ahfe2020/results_left_u-turn`.
2. In order to obtain trajectory data by rerunning driving simulations, scripts are provided for left and right U-turns.
```
python left_u-turn.py

python right_u-turn.py
```
