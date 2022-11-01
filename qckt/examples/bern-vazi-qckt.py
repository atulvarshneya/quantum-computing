#!/usr/bin/env python


print("""
-------------------------------------------------------------------------------------------------------
Problem Statement:

    Given a function f(x) on n qubits |x>, that has an n-bit secret code, a,
    with f(x) = a.x = (a0x0+a1x1+...) modulo 2.

    Find the secret code, a.
-------------------------------------------------------------------------------------------------------
""")

import qckt
from QSystems import *
from Job import Job
import Registers as regs
import random as rand

## The function with the secret code
def get_fxop(inreg, outreg):
	## fx has inreg register as inputs, and one qubit output
	inregsz = len(inreg)
	outregsz = len(outreg) # ASSERTION: outreg size is 1
	secret_code = rand.randint(0,2**inregsz-1)
	print(("Pssst... the secret code is {:0"+str(inregsz)+"b}").format(secret_code))

	fxckt = qckt.QCkt(inregsz+outregsz)
	for i in range(inregsz):
		if secret_code & (0x1<<i):
			fxckt.CX(inreg[inregsz-1-i],outreg[0])
	# fxckt.draw()
	return fxckt.to_opMatrix()

## Bern-Vazi algorithm
fxsize = 6
fxin = regs.QRegister(fxsize)
fxout = regs.QRegister(1)
rdout = regs.CRegister(fxsize)
nqubits, nclbits, _, _ = regs.placement(fxout, fxin, rdout)

print("Getting the secret function box...")
fxop = get_fxop(fxin,fxout)
print("OK, FX is ready.")

bv_ckt = qckt.QCkt(nqubits, nclbits)

# Step 0: Prepare the result bit |b> to |->
bv_ckt.X(fxout)
bv_ckt.H(fxout)

# Step 1: Apply H on all qbits of |x>
bv_ckt.H(fxin)

# Step 2: Now apply the secret function f()
bv_ckt.Border()
bv_ckt.CUSTOM("fx",fxop, fxout+fxin) # NOTE: placement() put fxout in MSB position so fxop requires fxout in MSB position
bv_ckt.Border()

# Step 3: Again apply H on all qbits of |x>
bv_ckt.H(fxin)

# Step 4: Measure all qbits of |x>
bv_ckt.M(fxin, rdout)

bv_ckt.draw()

job = Job(bv_ckt,qtrace=False)
Qdeb().runjob(job)
print(job.get_creg()[0])
