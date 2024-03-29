# Adding music effects to audio using ADSP-21489 development environment

## About the project

<p align="justify">This repository is associated with the Digital Signal Processing Systems course in the academic year 2023/2024, at the Faculty of Electrical Engineering in Banja Luka. The project itself focuses on implementing audio effects applicable to an audio signal, addressing requirements such as generating reference signals in Python, effect implementation on the ADSP processor, performance analysis and optionally, correcting algorithm implementation on the DSP. Implemented effects within this repository include Delay, Echo, Flanger, Tremolo and Bit crusher, written in Visual Studio Code and located in the 'python' subfolder. The C implementation is in the 'CCES' subfolder, utilizing the CCES development environment designed for the targeted ADSP-1489 platform. The 'docs' subfolder contains documentation, along with the working version of the report (in Serbian language).

## How to run the programs
### Python
Open main.py in VS Code or some other text editor to run Python script. Optionally, run it within cmd or git bash (inside folder it's contained), by entering following command:
```
python guitar_effects.py
```

### C
<p align="justify"> It's necessary to install CrossCore® Embedded Studio, specialized for working with DSP processors. Clone the repository and open project within CCES. 
Build project, and to run 'Debug', set Debug Configuration to SHARC -> ADSP-21489 -> EZ-KIT or Simulation. For the purposes of this project, ADSP-21489 EzKit board was used.

NOTE: After running 'Debug' in CCES, files with processed samples will be placed in Debug folder of the project. In this case, .txt files and generated .wav recordings can be found in the python folder of this repository, as there was a frequent need to change the project's workspace. Generated .wav files can be listened to using Audacity.
