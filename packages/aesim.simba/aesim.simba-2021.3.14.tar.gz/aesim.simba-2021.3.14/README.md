# SIMBA Python API

The Simba Python Module (aesim.simba) is a Python package that contains hundreds of functions providing direct access to SIMBA such as creating a circuit, modifying parameters, running a simulation, and retrieving results. aesim.simba is independent and does not require to have SIMBA installed to be used.

## Installation

The easiest way to install the Python API is using pip:

`pip install aesim.simba`

## Requirements

The current version of _aesim.simba_ is only compatible with Windows.

## Activation
The deployment key available on your [account profile page](https://www.simba.io/profile_account/) must be used to activate _aesim.simba_. Two methods are available:

### Using Environment Variable

The easiest way to activate pysimba is to set the environment variable `SIMBA_DEPLOYMENT_KEY` value to your deployment key. To add a new environment variable in Windows: 

* Open the Start Search, type in “env”, and choose “Edit the system environment variables”:
* Click the “Environment Variables…” button.
* Set the environment variables as needed. The New button adds an additional variable.

### Code-based Activation

The _License_ API can be also used to activate _aesim.simba_.

``` python
from aesim.simba import License
License.Activate('*** YOUR DEPLOYMENT KEY ***')
```

## API Documentation
The API documentation is available [here](https://www.simba.io/doc/python_api/api_index/). 

## Performance
Running a simulation using the Python API is significantly faster than using the SIMBA User Interface because there is no overhead.

## Quick Example
The following example opens the Flyback Converter Example available in SIMBA, runs it, and plots the output voltage.

``` python
#%% Load modules
from aesim.simba import DesignExamples
import matplotlib.pyplot as plt

#%% Load project
flybackConverter = DesignExamples.DCDC_Flyback()

#%% Get the job object and solve the system
job = flybackConverter.TransientAnalysis.NewJob()
status = job.Run()

#%% Get results
t = job.TimePoints
Vout = job.GetSignalByName('R2 - Instantaneous Voltage').DataPoints

#%% Plot Curve
fig, ax = plt.subplots()
ax.set_title(flybackConverter.Name)
ax.set_ylabel('Vout (V)')
ax.set_xlabel('time (s)')
ax.plot(t,Vout)

# %%
```
## More Examples
A collection of simple Python script examples using the SIMBA Python API is available on this [GitHub repository](https://github.com/aesim-tech/simba-python-examples)

## Public Beta
SIMBA is currently in public beta and can be **used by everyone for free**. The objective of this public beta is to gather feedback from users. Feel free to use our [public GitHub project](https://github.com/aesim-tech/simba-project) to check and contribute to our roadmap.

Copyright (c) 2019-2020 AESIM.tech