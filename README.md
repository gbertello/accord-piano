# Install

## Package manager

This program has been coded on a Mac OS environment. You will find detailed instructions for a Mac OS platform. As a first step, install brew as a package manager.
```
https://brew.sh/
```

For other platforms, use the package manager you are familiar with, given that it is purely optional (the dependencies can be installed without it).

## Python3
This program is coded in Python. Install python language on your operating system

For MacOS users:
```
brew install python3
```

For other platforms, you will find instructions on the Python3 User Guide page:
https://www.python.org/

Make sure the python version is correctly installed with its package manager pip3. The following commands should return no error.
```
python3 --version
pip3 --version
```

## Tkinter
This program uses tkinter as user interface. It is required to install it. 

For MacOS users:
```
brew install python-tk
```

For other platforms, you will instructions on the Tkinter User Guide page:
https://docs.python.org/fr/3/library/tkinter.html

## Python libraries
Python libraries can be installed with the help of virtualenv, which is used to install python packages on an isolated environment. It is strongly recommended to use it to avoid polluting the operating system. Normally, it should already been installed with your python installation. In case it is not check the virtualenv User Guide: https://virtualenv.pypa.io/en/latest/installation.html

Create a new virtual environment for python
```
python3 -m venv .venv
```

Activate the new virtual environment
```
source .venv/bin/activate
```

Install the python libraries
```
pip3 install -r requirements.txt
```

# Run
To run the program, launch the entry file accord.py
```
./accord.py
```

# Setup
To setup the program preferences, open the settings window by clicking on the "Settings" button.

## Device
Choose the device to record the piano sound. Usually, laptop microphone is fine.

## Sample rate
For best quality, use the highest possible sample rate (for example 192000 samples / second)

## Channels
Use this program in 1 channel (mono) as it is not intended for listening purposes.

## Interval
This setting is the delay between matplotlib frames in milliseconds. Use the default setting 30ms.

## Duration
This is the duration in seconds of the recording window for the sound. Use a large value for low pitches (30s) and a low value for high pitches (1s).

## Zoom
This is the ratio around which the axis window will be displayed. Start with the default value and play with the setting to adjust the window length. It is expressed in percentage of the frequency. (Ex: 8% zoom for a 440Hz A4 will display a window between 405 Hz and 475 Hz)

## Number of harmonics
This settings defines the number of harmonics to be computed. Usually, 12 can be computed for low sounds, 6 for medium sounds, 2-3 for very high sounds.

## Figure width
This is to adjust the number of windows per row in the matrix of harmonics. A figure width of 3 for 6 harmonics will display 2 rows.

## Inharmonicity
Piano harmonics are not pure multiples. For example a A4 with frequency 442 Hz will have its second harmonic at around 883 Hz. In this example, the inharmonicy factor will be 400 * log2(883/882) = 0.654

This is piano dependent and will have to be computed in each situation. 

For advanced users, it corresponds to the K factor in this paper.
http://www.temperamentcordier.org/inharmonicite/Memoireinharmonicite%20.pdf

## Inharmonicity ratio
Inharmonicity factor increases with frequency. It is often set around 10 ^ 0.04 = 1.096

This is piano dependent and will have to be computed in each situation. 

For advanced users, it corresponds to the q factor in this paper.
http://www.temperamentcordier.org/inharmonicite/Memoireinharmonicite%20.pdf

# Advanced estimation of inharmonicity

Mathematical works have been filed in the folder called "Inharmonicite". It consists of a series of mathematical operations based on a pre-recorded of piano string samples in isolation. For a pitch with multiple strings, only 1 string has been recorded (for example 1 string out of 3 on A4).

## Get harmonics
This function returns the harmonics of the recorded sounds

## Get stiffness
This function estimates the stiffness of the recorded sounds. It is based on the formula fn = n * sqrt(1 + B * n^2) * f0 explained in this page: https://fr.wikipedia.org/wiki/Inharmonicit%C3%A9

## Model stiffness
This function models the stiffness based on a polynomial assumption (degree 4)

## Estimate error
This function estimates the error between the estimated stiffness by model and the measured stiffness

## Find inharmonicity
This function estimated the inharmonicity factor for the A4 string. It correspond to the Inharmonicity setting of the settings window

## Find inharmonicity ratio
This function estimated the inharmonicity ratio for the entire piano. It correspond to the Inharmonicity Ratio setting of the settings window
