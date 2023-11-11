#!/usr/bin/env python

import qckt
from qckt.backend import *
import random as rnd
import numpy as np

ufinpsz = 4
inpreg = qckt.QRegister(ufinpsz)
clmeas = qckt.CRegister(ufinpsz)
nqubits,nclbits,_,_ = qckt.placement(inpreg,clmeas)

### Uf - The oracle (the verifying function, the database lookup)
marked = int(rnd.random()*2**nqubits)
print("Oracle 'marked one' = ",("{:0"+str(nqubits)+"b}").format(marked))
uf_ckt = qckt.QCkt(nqubits,name="Uf Invert")
zeros = []
for i in range(len(inpreg)):
	if (marked & (1 << i)) == 0:
		zeros.append(inpreg[-i-1])
uf_ckt.Border()
if len(zeros) > 0:
	uf_ckt.X(zeros)
uf_ckt.CZ(*inpreg)
if len(zeros) > 0:
	uf_ckt.X(zeros)
uf_ckt.Border()
# uf_ckt.draw()

### Initialize
initckt = qckt.QCkt(nqubits,name="Initialize")
initckt.H(inpreg)
# initckt.draw()

### amplify
ampckt = qckt.QCkt(nqubits,name="Amplify")
ampckt.H(inpreg)
ampckt.X(inpreg)
ampckt.CZ(*inpreg)
ampckt.X(inpreg)
ampckt.H(inpreg)
# ampckt.draw()

fullckt = qckt.QCkt(nqubits,nclbits,name="Full Circuit")
fullckt = fullckt.append(initckt)
numitrs = int((np.pi/4.0)*(2.0**(nqubits/2.0))) # optimal # iter, less or more dont work
print("INVERT(Uf)-AMPLIFY iterations = ",numitrs)
for i in range(numitrs):
	fullckt = fullckt.append(uf_ckt)
	# fullckt.Probe('Invert',probestates=[marked-1, marked, marked+1])
	fullckt = fullckt.append(ampckt)
	# fullckt.Probe('Iteration {:d}'.format(i+1),probestates=[marked-1, marked, marked+1])
fullckt.M(inpreg,clmeas)
fullckt.draw()

nattempts = 5
stats = {}
for _ in range(nattempts):
	job = qckt.Job(fullckt)
	bk = Qdeb()
	bk.runjob(job)
	creg = job.get_creg()[0]
	svec = job.get_svec()
	# print(svec.value[marked][0])
	print("Search result = ",creg)
	if str(creg) in stats.keys():
		stats[str(creg)] += 1
	else:
		stats[str(creg)] = 1

maxkey = ""
maxcount = 0
for k in stats.keys():
	if stats[k] > maxcount:
		maxkey = k
		maxcount = stats[k]
print("Result = {0:s}, with {1:d} hits in {2:d}.".format(maxkey,maxcount,nattempts))
