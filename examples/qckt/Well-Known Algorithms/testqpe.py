#!/usr/bin/env python

import numpy as np
import qckt
from qckt.backend import *
import libqpe as qpe

####
# qubits registers
# | target |    measurement qubits   |
# |  MSB   |   ... ... ... 2  1  0   |
####
n_counting_qubits = 4
measurement_qubits = [i for i in reversed(range(n_counting_qubits))]
target_qubit = [n_counting_qubits]
nqubits = n_counting_qubits + 1

####
# the target unitary operator (we do a 1 qubit function here), converted to an operator matrix
####
theta = 6.0/8.0
ckt = qckt.QCkt(1)
ckt.P(2*np.pi*theta,0)
uop = ckt.to_opMatrix()

####
# construct the QPE circuit
# create the initial part of the circuit,
# * with measurement qubits register, and 
# * target uop register, setup with an eigenvector
# add the full QPE circuit built using libqpe QPE class
# finally, the measurement of measuremnt_qubits
#
# libqpe QPE class takes as inputs:
# * the unitary operator,
# * a register on which the operator operates, initialized to an eigenvector of the operator, and
# * a register for measuring the result
####
# start the circuit
mycircuit = qckt.QCkt(nqubits=nqubits,nclbits=nqubits)
# set target register to operator's eigenvector
mycircuit.X(target_qubit)
# get the rest of the QPE circuit built using libqpe
qpeckt = qpe.QPE(uop, target_qubit, measurement_qubits).getckt()
# append to the initial circuit
mycircuit = mycircuit.append(qpeckt)
# and add the measuremnt
mycircuit.M(measurement_qubits)
mycircuit.draw()

####
## run multiple shots display the bargraph of results
## pick the one with max freq as the result
####
job = qckt.Job(mycircuit, shots=100)
bk = Qeng()
bk.runjob(job)
creg = job.get_creg()
counts = job.get_counts()

# use the measured values to compute estimated phase
resvalue = max(range(len(counts)), key=lambda x : counts[x])
print(f"Most frequent readout = {resvalue},  frequency = {counts[resvalue]}/{len(creg)}")
print(str(resvalue)+"/2**"+str(n_counting_qubits)," = ",float(resvalue)/(2**n_counting_qubits))
