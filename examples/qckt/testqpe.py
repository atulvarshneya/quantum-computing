#!/usr/bin/env python

import numpy as np
import qckt
from qckt.backend import *
import libqpe as qpe

n_counting_qubits = 4

measurement_qubits = qckt.QRegister(n_counting_qubits)
target_qubit = qckt.QRegister(1)
measurement_clbits = qckt.CRegister(n_counting_qubits)
nqubits,nclbits,qplaced,_ = qckt.placement(target_qubit, measurement_qubits, measurement_clbits)

theta = 6.0/8.0
ckt = qckt.QCkt(1)
ckt.P(2*np.pi*theta,0)
uop = ckt.to_opMatrix()
mycircuit = qckt.QCkt(nqubits,nclbits)
mycircuit.X(target_qubit)
qpeckt = qpe.QPE(uop, target_qubit, measurement_qubits).getckt()
mycircuit = mycircuit.append(qpeckt)
mycircuit.M(measurement_qubits, measurement_clbits)
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

resvalue = max(range(len(counts)), key=lambda x : counts[x])
print(f"Most frequent readout = {resvalue},  frequency = {counts[resvalue]}/{len(creg)}")
print(str(resvalue)+"/2**"+str(n_counting_qubits)," = ",float(resvalue)/(2**n_counting_qubits))
