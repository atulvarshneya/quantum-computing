# quantum-computing

A functionally complete simulator for Universal Quantum Computer in Python. Have tried upto 11 qubits on an old laptop (1 core, 1GB RAM). More compute+memory, more qubits.


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
* ... more added every few days
* Shore's algorithm coming soon

An interactive commandline interface (qc-cli.py) to quickly check out operations and sequences.


GATES
-------------------
All commonly used gates included 
* Hadamard
* CNOT
* SWAP
* CSWAP
* SQSWAP (square root of SWAP)
* Toffoli
* Pauli_x
* Pauli_y
* Pauli_z
* Phase rotation by phi
* Phase rotation by 2*pi/(2^k)
* n-qubit QFT
* n-qubit Hadamard

Create a CONTROLLED GATE for any given gate; add any number of control qubits.

Allows addition of any user-defined gates.

BASIS
-------------------
Common basis for measurement are included - Bell-Basis, |+>/|->.

Allows addition of any user-defined bases.

UTILITIES
-------------------
A number of utility functions to manipulate gates - combine sequentially applied, or parallelly applied gates into a single gate, check for unitarity, inverse.

Easy to follow documentation with tutorial introduction. See qclib-doc.txt (https://raw.githubusercontent.com/atulvarshneya/quantum-computing/master/qclib-doc.txt).

Code for [automated] regression tests also serves as examples to quickly learn qclib.
