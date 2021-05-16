#!/usr/bin/python3

import qckt
from QSystems import *
from Job import Job
import Registers as regs
import numpy as np
import random as rnd

#################################################################################
# Details @ https://en.wikipedia.org/wiki/Grover%27s_algorithm
#################################################################################

ufinpsz = 6
inpreg = regs.QRegister(ufinpsz)
outreg = regs.QRegister(1)
clmeas = regs.CRegister(ufinpsz)
nqbits,ncbits,_,_ = regs.placement(outreg,inpreg,clmeas)

# 'needle' in the haytack = key
marker = int(rnd.random() * (2**(nqbits-1)-1))
print(("Marker to search = {0:0"+str(nqbits-1)+"b}, ({0:d})").format(marker))
uf_ckt = qckt.QCkt(nqbits,name="Uf")
uf_ckt.Border()
x_list = []
for i in range(len(inpreg)):
	if (marker & (0b1<<i)) == 0:
		x_list.append(inpreg[-i-1]) # index i backwards from the end of inpreg
if len(x_list) > 0:
	uf_ckt.X(x_list)
uf_ckt.CX(*(inpreg+outreg)) # target of the CX operation is outreg qubit
if len(x_list) > 0:
	uf_ckt.X(x_list)
uf_ckt.Border()
# uf_ckt.draw()

amp_ckt = qckt.QCkt(nqbits,name="Diffuser")
amp_ckt.H(inpreg)
amp_ckt.X(inpreg)
amp_ckt.CX(*(inpreg+outreg))   ## This is how Umesh Vazirni explains it
# amp_ckt.CZ(*inpreg) ## Gives identical results ... since still invertig phase of the inputs register.
amp_ckt.X(inpreg)
amp_ckt.H(inpreg)
# amp_ckt.draw()

init_ckt = qckt.QCkt(nqbits,name="Initialize")
init_ckt.H(inpreg)
# setup the result qubit in |-> state for phase kickback
init_ckt.X(outreg)
init_ckt.H(outreg)
# init_ckt.draw()

fullckt = qckt.QCkt(nqbits,ncbits,name="Full Grover's Circuit")
fullckt = fullckt.append(init_ckt)
fullckt.Probe("after initialization", probestates=[marker])
numitrs = int((np.pi/4.0) * (2.0**((nqbits-1.0)/2.0))) # optimal # iter, less or more dont work
print("number of Invert-Diffuser iterations = ",numitrs)
for itr in range(numitrs):
	fullckt = fullckt.append(uf_ckt)
	fullckt = fullckt.append(amp_ckt)
	fullckt.Probe("after iteration "+str(itr+1), probestates=[marker])
fullckt.M(inpreg,clmeas)
# print("### Grover's Circuit ################################")
# fullckt.draw()

maxattempts = 5
for m in range(maxattempts):  # Look for best of all attempts
	job = Job(fullckt)
	bk = Qdeb()
	bk.runjob(job)
	res = job.get_creg()[0]
	print("Result = ",res.intvalue)
	print()

	### Verify if the resultis correct
	vrinpreg = regs.QRegister(ufinpsz)
	vroutreg = regs.QRegister(1)
	vrclmeas = regs.CRegister(1)
	vrnq,vrnc,_,_ = regs.placement(vroutreg,vrinpreg,vrclmeas)
	verifyckt = qckt.QCkt(vrnq,vrnc,name="Verify")
	x_list = []
	for i in range(len(vrinpreg)):
		if (res.intvalue & (0b1<<i)) != 0:
			x_list.append(vrinpreg[-i-1])
	if len(x_list) > 0:
		verifyckt.X(x_list)
	verifyckt = verifyckt.append(uf_ckt)
	verifyckt.M(vroutreg,vrclmeas)
	# print("### Verification Circuit ################################")
	# verifyckt.draw()

	job = Job(verifyckt)
	bk = Qdeb()
	bk.runjob(job)
	creg = job.get_creg()[0]
	if creg.intvalue == 1:
		print("CORRECT Result in ",m+1,"attempts")
		break
