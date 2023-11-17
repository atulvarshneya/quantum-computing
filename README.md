# quantum-computing

A functionally complete Universal Quantum Computer in Python.

Comprises of two parts - qusimulator (package qsim) the Quantum Simulator, and qucircuit (packages qckt, qckt.gatesutils, and qckt.backend) the library to implement quantum computing programs using Quantum Circuits. qucircuit uses qusimulator as a backed engine to execute quantum circuits

INSTALLING
-------------------
qusimulator and qucircuit are on PyPi now. So, you can simply install them using pip. Since qucircuit has qusimulator as a dependency, so installing qucircuit will also install qusimulator.

    pip install qusimulator
    pip install qucircuit

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
All common gates included. Can create CONTROLLED GATE for any gates.  Allows addition of CUSTOM user-defined gates.

A number of utility functions to manipulate gates - combine sequentially applied, or parallelly applied gates, check for unitarity, inverse.

QUANTUM CIRCUITS AND BACKEND COMPUTE ENGINES
-------------------

Quantum computing circuits framework with a backend compute simulator engine.

Easy to follow documentation with tutorial introduction - see qusimumator/README.md and qucircuit/README.md. A bunch of examples under qusimulator/examples and qucircuit/examples.

Code for regression tests also serves as examples to quickly learn qsim and qckt packages.
