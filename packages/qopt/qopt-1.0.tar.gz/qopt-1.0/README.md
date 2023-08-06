# qopt: A Simulation and Quantum Optimal Control Package

## Documentation
The documentation can be found on 
[readthedocs](https://qopt.readthedocs.io/en/latest/index.html). 
It features an API documentation and an introduction in the 
form of jupyter notebooks demonstrating how to utilize the package.


## Introduction
In current quantum computer prototypes information is stored and processed in 
quantum bits or qubits which are controlled e.g. by electric pulses. In order 
to find the optimal control pulse for a given operation, this package simulates 
the system under control and applies optimization algorithms to the pulses. 
These include gradient based algorithms generalizing the GRAPE algorithm [1].

The package sets a focus on realistic noise models to enable noise mitigation
through pulse tailoring. Imperfections of the control electronics can also be
included in the simulations.

The implementation was inspired by the optimal control package of 
[QuTiP](http://qutip.org/).

## Installation
The recommended way is to use conda for the installation.
To avoid difficulties, QuTiP needs to be installed first. To do so, follow 
[their instructions](http://qutip.org/docs/latest/installation.html) or these
instructions. Usually it is most convenient to create a new environment. The 
package was written and tested using python 3.7.

    conda create --name qopt_env python=3.7
    conda activate qopt_env

Start with all recommended dependencies: 

    conda install numpy scipy cython matplotlib pytest pytest-cov jupyter

Then open a conda forge channel:

    conda config --append channels conda-forge
    
and install QuTiP:

    conda install qutip

Then install two remaining dependencies and the 
[filter_functions package](https://github.com/qutech/filter_functions) via pip:

    conda install pandas simanneal
    pip install filter_functions
    
And either install qopt via pip 

    pip install qopt

or alternatively download the source code and use
`python setup.py develop` to install using symlinks or 
`python setup.py install` without.

## References
[1]: Khaneja, N., Reiss, T., Kehlet, C., Schulte-Herbrüggen, T., Glaser, S.
(2004). Optimal control of coupled spin dynamics: design of NMR pulse sequences
gy gradient ascent algorithms 
[https://doi.org/10.1016/j.jmr.2004.11.004](https://doi.org/10.1016/j.jmr.2004.11.004)