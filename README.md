# quantum-computing

A functionally complete simulator for Universal Quantum Computer in Python. Have tried upto 11 qubits on an old laptop (1 core, 1GB RAM).

Comprises of two parts - qsim the Quantum Simulator, and qckt - to implement quantum computing programs using Quantum Circuits with qsim as a backed to execute the quantum circuits

INSTALLING
-------------------
mkdir yourdir
cd yourdir
git clone https://github.com/atulvarshneya/quantum-computing.git
cd quantum-computing
./pip-install.sh


FEATURES
-------------------
All expected features and more, simple to use, extensible and flexible to allow all aspects of quantum computing. Flexible, because you write the algorithms in a regular programming language, Python, so no limitations on the program logic, the simulator API abstracts a Universal Quantum Computer as a backend resource.

Can implement any quantum computing algorithms. Several algorithm implementations included as examples:
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


GATES
-------------------
All commonly used gates included.

Can create CONTROLLED GATE for any given gate; add any number of control qubits.

Allows easy addition of user-defined gates.


UTILITIES
-------------------
A number of utility functions to manipulate gates - combine sequentially applied, or parallelly applied gates into a single gate, check for unitarity, inverse.

Easy to follow documentation with tutorial introduction - see qsim/README.md and qckt/README.md.

Code for [automated] regression tests also serves as examples to quickly learn qsim and qckt.
