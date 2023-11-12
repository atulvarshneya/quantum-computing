# quantum-computing

A functionally complete Universal Quantum Computer in Python.

Comprises of two parts - qsim the Quantum Simulator, and qckt - to implement quantum computing programs using Quantum Circuits with qsim as a backed engine to execute the quantum circuits

INSTALLING
-------------------
mkdir yourdir
cd yourdir
git clone https://github.com/atulvarshneya/quantum-computing.git
cd quantum-computing
./pip-install.sh


FEATURES
-------------------
All expected features, simple to use, extensible and flexible to allow all aspects of quantum computing.

Implement any quantum computing algorithms. Several algorithm implementations included as examples:
* Teleportation
* Simple Search
* Deutsch-Jozsa
* Bernstien-Vazirani
* Quantum Fourier Tramsform
* Period-finding
* Grover's algorithm
* Sudoku using Grover's algorithm
* ... will add more as I get a chance

An interactive commandline interface (qcli.py) to quickly check out operations and sequences.


GATES AND UTILITIES
-------------------
All standard gates included. Can create CONTROLLED GATE for any gates.  Allows addition of CUSTOM user-defined gates.

A number of utility functions to manipulate gates - combine sequentially applied, or parallelly applied gates, check for unitarity, inverse.

QUANTUM CIRCUITS AND BACKEND COMPUTE ENGINES
-------------------

Quantum computing circuits framework with a backend compute simulator engine.

Easy to follow documentation with tutorial introduction - see qsimumator/README.md and qcircuit/README.md. A bunch of examples under qsimulator/examples and qcircuit/examples.

Code for regression tests also serves as examples to quickly learn qsim and qckt.
