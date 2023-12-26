#!/usr/bin/env python

import numpy as np
import qckt
from qckt.backend import *
import libqpe as qpe

n_counting_qubits = 4

measurement_qubits = qckt.QRegister(n_counting_qubits)
gap1 = qckt.QRegister(1)
target_qubit = qckt.QRegister(1)
gap2 = qckt.QRegister(1)
measurement_clbits = qckt.CRegister(n_counting_qubits)
nqubits,nclbits,qplaced,_ = qckt.placement(gap1, target_qubit, measurement_qubits, gap2, measurement_clbits)

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
## pick the one with max freq as teh result
####

readouts = {}
maxreads = 0
resvalue = None
for i in range(100):
	job = qckt.Job(mycircuit)
	bk = Qdeb()
	bk.runjob(job)

	readval = (job.get_creg()[0]).intvalue
	if readval in readouts.keys():
		readouts[readval] += 1
	else:
		readouts[readval] = 1
	if readouts[readval] > maxreads:
		resvalue = readval
		maxreads = readouts[readval]

minkey = min(readouts.keys())
maxkey = max(readouts.keys())

barsize = 100
barscale = float(barsize)/maxreads

for i in range(minkey,maxkey+1):
	print("{:6d}  ".format(i),end="")
	if i in readouts.keys():
		for j in range(int(readouts[i]*barscale)):
			print("#",end="")
	print()

print("Max frequency = ",maxreads)
print(str(resvalue)+"/2**"+str(n_counting_qubits)," = ",float(resvalue)/(2**n_counting_qubits))
