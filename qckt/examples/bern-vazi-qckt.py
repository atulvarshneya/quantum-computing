#!/usr/bin/python3

import qckt
from QSystems import *
import random as rand

print("""
-------------------------------------------------------------------------------------------------------
Problem Statement:

    Given a function f(x) on n qubits |x>, that has an n-bit secret code, a,
    with f(x) = a.x = (a0x0+a1x1+...) modulo 2.

    Find the secret code, a.
-------------------------------------------------------------------------------------------------------
""")

###########################################################################
## This is the function with the secret code
###########################################################################
def get_fxckt(nq):
	nqubits = nq
	## fx has nqubits -1 inputs, and the remaining one qubit is the output
	secret_code = rand.randint(0,2**(nqubits-1)-1)
	code_fmt = "{:0"+"{:d}".format(nqubits-1)+"b}"
	print("Pssst... the secret code is ",code_fmt.format(secret_code))
	fxckt = qckt.QCkt(nqubits)
	for i in range(nqubits-1):
		if secret_code & (0x1<<i):
			fxckt.CX(i,nqubits-1)
	# fxckt.draw()
	return fxckt

class bernvazi:
	def __init__(self, qsimsz):
		self.nqubits = qsimsz
		self.nclbits = qsimsz

	def gen_bv_ckt(self):
		print("Getting the secret function box...")
		fxckt = get_fxckt(self.nqubits) # returns FX that acts on self.nqubits qbits
		print("OK, FX is ready.")

		###########################################################################
		## Start of the Bernstien-Vazirani algorithm
		###########################################################################
		print()
		print("Starting the BV algorithm...")

		###########################################################################
		# Step 0: Prepare the result bit |b> to |->
		bv_ckt = qckt.QCkt(self.nqubits, self.nclbits)
		bv_ckt.X(self.nqubits-1)
		bv_ckt.H(self.nqubits-1)
		print("Step 0: Prepared |b> as |->")
		# bv_ckt.draw()

		###########################################################################
		## Step 1: Apply H on all qbits of |x>
		for i in range(self.nqubits-1):
			bv_ckt.H(i)
		print("Step 1: Applied H to all |x> qbits")
		# bv_ckt.draw()

		###########################################################################
		## Step 2: Now apply the secret function f()
		bv_ckt.Border()
		### not sure why this code was there at all
		### as realign() was defined at that time, these two lines is basically a NOOP
		### qbit_list = list(range(self.nqubits))
		### fxckt = fxckt.realign(self.nqubits,self.nqubits,qbit_list)
		bv_ckt = bv_ckt.append(fxckt)
		bv_ckt.Border()
		print("Step 2: Applied FX to |b>|x>")
		# bv_ckt.draw()

		###########################################################################
		## Step 3: Again apply H on all qbits of |x>
		for i in range(self.nqubits-1):
			bv_ckt.H(i)
		print("Step 3: Again Applied H to all |x> qbits")
		# bv_ckt.draw()

		###########################################################################
		## Step 4: Measure all qbits of |x>
		bv_ckt.M(list(range(self.nqubits-1)))
		print("Step 4: measure all |x> qbits")
		# bv_ckt.draw()

		return bv_ckt


if __name__ == "__main__":
	nqubits = 8
	bv = bernvazi(nqubits)
	bv_ckt = bv.gen_bv_ckt()
	bk = Backend()
	bk.run(bv_ckt,qtrace=False)
	print(bk.get_creg())
