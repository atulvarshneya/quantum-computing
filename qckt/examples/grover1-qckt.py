#!/usr/bin/python3

import qckt
from QSystems import *
import numpy as np
import random as rnd

#################################################################################
# Details @ https://en.wikipedia.org/wiki/Grover%27s_algorithm
#################################################################################

nqbits = 7

# 'needle' in the haytack = key
marker = int(rnd.random() * (2**(nqbits-1)-1))
print(("Marker to search = {0:0"+str(nqbits-1)+"b}, ({0:d})").format(marker))
uf_ckt = qckt.QCkt(nqbits,name="Uf")
uf_ckt.Border()
x_list = []
for i in range(nqbits-1):
	if (marker & (0b1<<i)) == 0:
		x_list.append(i)
uf_ckt.X(x_list)
uf_ckt.CX(*[i for i in range(nqbits)])
uf_ckt.X(x_list)
uf_ckt.Border()
# uf_ckt.draw()

amp_ckt = qckt.QCkt(nqbits,name="Diffuser")
amp_ckt.H([i for i in range(nqbits-1)])
amp_ckt.X([i for i in range(nqbits-1)])
amp_ckt.CX(*[i for i in range(nqbits)])   ## This is how Umesh Vazirni explains it
# amp_ckt.CZ(*[i for i in range(nqbits-1)]) ## Gives identical results ... since still invertig phase of the inputs register.
amp_ckt.X([i for i in range(nqbits-1)])
amp_ckt.H([i for i in range(nqbits-1)])
# amp_ckt.draw()

init_ckt = qckt.QCkt(nqbits,name="Initialize")
init_ckt.H([i for i in range(nqbits-1)])
# setup the result qubit in |-> state for phase kickback
init_ckt.X(nqbits-1)
init_ckt.H(nqbits-1)
# init_ckt.draw()

fullckt = qckt.QCkt(nqbits,nqbits,name="Full Grover's Circuit")
fullckt = fullckt.append(init_ckt)
fullckt.Probe("after initialization", probestates=[marker])
numitrs = int((np.pi/4.0) * (2.0**((nqbits-1.0)/2.0))) # optimal # iter, less or more dont work
print("number of Invert-Diffuser iterations = ",numitrs)
for itr in range(numitrs):
	fullckt = fullckt.append(uf_ckt)
	fullckt = fullckt.append(amp_ckt)
	fullckt.Probe("after iteration "+str(itr+1), probestates=[marker])
fullckt.M([i for i in range(nqbits-1)])
# print("### Grover's Circuit ################################")
# fullckt.draw()

maxattempts = 5
for m in range(maxattempts):  # Look for best of all attempts
	bk = Backend()
	bk.run(fullckt)
	res = bk.get_creg()
	print("Result = ",res.intvalue)
	print()

	### Verify if the resultis correct
	verifyckt = qckt.QCkt(nqbits,nqbits,name="Verify")
	x_list = []
	for i in range(nqbits-1):
		if (res.intvalue & (0b1<<i)) != 0:
			x_list.append(i)
	verifyckt.X(x_list)
	verifyckt = verifyckt.append(uf_ckt)
	verifyckt.M([nqbits-1],[0])
	# print("### Verification Circuit ################################")
	# verifyckt.draw()

	bk = Backend()
	bk.run(verifyckt)
	creg = bk.get_creg()
	if creg.intvalue == 1:
		print("CORRECT Result in ",m+1,"attempts")
		break
