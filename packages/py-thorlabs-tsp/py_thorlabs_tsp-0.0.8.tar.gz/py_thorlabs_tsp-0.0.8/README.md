# py_thorlabs_tsp

Low and high level python wrappers for Thorlabs TSP01B temperature and humidity
sensor. 

This is an unofficial package and is not supported by the vendor 
of equipment.

This package provides: 
1. low-level functions, which are thin wrappers around the C-functions
from the DLL distributed by Thorlabs; 
2. high-level class for connecting to the sensor and getting temperature and 
humidity readout.

This package was tested on Windows only. Only TSP01 **Rev.B** sensor was 
tested. 

Installation
------------
#### Prerequisites

Download and install the software from 
[thorlabs.com](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=5884), 
choose *Software* tab. 
This program provides the drivers (DLLs discoverable by the py_thorlabs_tsp), 
and also the *TSP01 Application*, which has a GUI and allows connecting
and reading out the sensor.

The package itself can be installed either from pypi or from the repository.
See both options below. 

#### From pypi

1. Install the package from pypi:
    
    `$ pip install py_thorlabs_tsp`

#### From repository

1. Clone the package from the repository

    `$ git clone https://gitlab.com/dimapu/py_thorlabs_tsp.git py_thorlabs_tsp_repo`

2. Install py_thorlabs_tsp either in normal mode:
    
    `$ pip install py_thorlabs_tsp_repo` 
    
    OR in development mode:
    
    `$ pip install -e py_thorlabs_tsp_repo` 

Authors
-------
The following authors have contributed to this package:
 * Dzmitry Pustakhod (original Windows version).


License
-------
Copyright (c) 2019 Dzmitry Pustakhod, TU/e-PITC.

The code is released under MIT license. See LICENSE.

The descriptions of the functions and their parameters are taken from the 
Thorlabs Manual and are a copyright of Thorlabs. See LICENSE_THORLABS.
