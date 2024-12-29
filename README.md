# Install

## Package manager

I have coded this program on a Mac OS environment. You will find detailed instructions for a Mac OS platform. As a first step, install brew as a package manager.
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
