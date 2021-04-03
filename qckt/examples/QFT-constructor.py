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
        circuit.CP(np.pi/2**(n-qubit), qubit, n)
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

nqubits = 6

ck = qckt.QCkt(nqubits)
for i in range(nqubits // 2):
	ck.X(i)
ck.Border()
qft(ck,nqubits)
ck.Border()
ck.draw()
ck.list()
bk = qckt.Backend()
bk.run(ck)
svec1 = bk.get_svec()
print(svec1)

ck = qckt.QCkt(nqubits)
for i in range(nqubits // 2):
	ck.X(i)
ck.Border()
ck.QFT([5,4,3,2,1,0])
ck.Border()
ck.draw()
ck.list()
bk = qckt.Backend()
bk.run(ck)
svec2 = bk.get_svec()
print(svec2)

### compare the two svecs
maxerr = 1.0e-10
isequal = True
if len(svec1.value) != len(svec2.value):
	isequal = False
else:
	for i in range(len(svec1.value)):
		amp1 = svec1.value[i][0]
		amp2 = svec2.value[i][0]
		if abs(amp1.real - amp2.real) > maxerr or abs(amp1.imag - amp2.imag) > maxerr :
			print(f"i = {i:} is different", svec1.value[i][0], svec2.value[i][0])
			isequal = False
if isequal:
	print("QFT and composed-QFT circuit are equivalent")
else:
	print("ERROR: QFT and composed-QFT circuit are significantly different")
