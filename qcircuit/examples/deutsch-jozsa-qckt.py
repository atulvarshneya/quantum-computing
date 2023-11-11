#!/usr/bin/env python

import random as rnd
import numpy as np
import qckt
from qckt.backend import *

print("""
-------------------------------------------------------------------------------------------------------
Problem Statement:
  Given a function whose output is CONSTANT (fixed output in the result
  register) or BALANCED (result register is equally 0 and 1 across all
  possible input values. Problem is to find which fx it is.

This program randomly selects one of the two fx's and the algorithm
determines which one it is.
-------------------------------------------------------------------------------------------------------
""")

def get_fxckt(inpreg, outreg):
	fxckt = qckt.QCkt(len(inpreg+outreg))
	toss = int(rnd.random()*2.0)
	if toss == 0:
		print("fx is CONSTANT.")
	elif toss == 1:
		print("fx is BALANCED.")
		fxckt.CX(inpreg[-1],outreg[0])
	return fxckt


fxsize = 7
inpreg = qckt.QRegister(fxsize)
outreg = qckt.QRegister(1)
clmeas = qckt.CRegister(fxsize)
nqbits,ncbits,_,_ = qckt.placement(inpreg,outreg,clmeas)

dj_ckt = qckt.QCkt(nqbits,ncbits)

dj_ckt.X(outreg)
dj_ckt.H(outreg)
dj_ckt.H(inpreg)
dj_ckt.Border()
fx_ckt = get_fxckt(inpreg, outreg)
dj_ckt = dj_ckt.append(fx_ckt)
dj_ckt.Border()
dj_ckt.H(inpreg)
dj_ckt.M(inpreg,clmeas)

dj_ckt.draw()

job = qckt.Job(dj_ckt,qtrace=False, shots=1)
bk = Qdeb()
bk.runjob(job)
res = job.get_creg()[0]
print(res)

if 1 in res.value[1:nqbits]:
	print("Found fx is BALANCED")
else:
	print("Found fx is CONSTANT")

