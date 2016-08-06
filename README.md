# quantum-computing

Very complete Quantum Computing simulator in Python. Have tried upto 11 qubits on an ordinary laptop. More compute+memory, more qubits.

All expected features implemented, simple to use, flexible, can implement any quantum computing algorithm; several examples included (Teleportation, Bernstien-Vazirani, Quantum Fourier Tramsform, Period-finding ... more added on daily basis - Shores and Grover's algos coming soon).

All normally used gates included - Hadamard, Pauli_x, Pauli_y, Pauli_z, Phase rotation by phi, Phase rotation by 2*pi/(2**k), CNOT, SWAP, Toffoli - Create a controlled gate for any given gate; add any number of control qubits. Additionally, no restrictions to add user-defined gates.

Allows any user-defined bases for measurements. Bell-Basis, |+>/|-> basis included.

A number of utility functions to manipulate gates - combine sequentially applied, or parallelly applied gates into a single gate, check for unitarity, inverse.

Easy to follow documentation with tutorial introduction. See qclib/qclib-doc.txt.

Code for [automated] regression tests also serves as examples to quickly learn qclib.
