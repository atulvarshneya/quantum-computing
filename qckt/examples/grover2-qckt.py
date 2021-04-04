#!/usr/bin/python3

import qckt
import random as rnd
import numpy as np

nqubits = 4

### The oracle (the verifying function, the database lookup)
### Uf
marked = int(rnd.random()*2**(nqubits-1))
print("Oracle 'marked one' = ",("{:0"+str(nqubits)+"b}").format(marked))
uf_ckt = qckt.QCkt(nqubits)
zeros = []
for i in range(nqubits):
	if (marked & (1 << i)) == 0:
		zeros.append(i)
uf_ckt.Border()
uf_ckt.X(zeros)
uf_ckt.CZ(*list(range(nqubits)))
uf_ckt.X(zeros)
uf_ckt.Border()

### Initialize
###
initckt = qckt.QCkt(nqubits)
initckt.H([i for i in range(nqubits)])
# print("===INITIALIZE===")
# initckt.draw()

# print("===Uf (INVERT)==")
# uf_ckt.draw()

### amplify
###
ampckt = qckt.QCkt(nqubits)
ampckt.H([i for i in range(nqubits)])
ampckt.X([i for i in range(nqubits)])
ampckt.CZ(*[i for i in range(nqubits)])
ampckt.X([i for i in range(nqubits)])
ampckt.H([i for i in range(nqubits)])
# print("===AMPLIFY======")
# ampckt.draw()

fullckt = qckt.QCkt(nqubits)
fullckt = fullckt.append(initckt)
numitrs = int((np.pi/4.0)*(2.0**(nqubits/2.0))) # optimal # iter, less or more dont work
print("INVERT(Uf)-AMPLIFY iterations = ",numitrs)
for i in range(numitrs):
	fullckt = fullckt.append(uf_ckt)
	# fullckt.Probe('Invert',probestates=[marked-1, marked, marked+1])
	fullckt = fullckt.append(ampckt)
	# fullckt.Probe('Iteration {:d}'.format(i+1),probestates=[marked-1, marked, marked+1])
fullckt.M([i for i in range(nqubits)])
# fullckt.draw()

stats = {}
for _ in range(5):
	bk = qckt.Backend()
	bk.run(fullckt)
	creg = bk.get_creg()
	svec = bk.get_svec()
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
print("Result = {0:s}, with {1:d} hits.".format(maxkey,maxcount))
