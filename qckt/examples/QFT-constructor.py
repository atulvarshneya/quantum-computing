#!/usr/bin/python3

import qckt
import numpy as np

def qft_rotations(circuit, n):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.H(n)
    for qubit in range(n):
        circuit.CROT(np.pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.SWAP(qubit, n-qubit-1)
    return circuit

def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

ck = qckt.QCkt(4)
ck.X(0)
ck.X(2)
qft(ck,4)
bk = qckt.Backend()
bk.run(ck)
print(bk.get_svec())

ck = qckt.QCkt(4)
ck.X(0)
ck.X(2)
ck.QFT([3,2,1,0])
bk = qckt.Backend()
bk.run(ck)
print(bk.get_svec())
