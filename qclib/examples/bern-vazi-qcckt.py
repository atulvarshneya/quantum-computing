#!/usr/bin/python3

import qcckt
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
	input_sz = nqubits - 1
	secret_code = rand.randint(0,2**input_sz-1)
	code_fmt = "{:0"+"{:d}".format(input_sz)+"b}"
	print("Pssst... the secret code is ",code_fmt.format(secret_code))
	fxckt = qcckt.QCkt(nqubits)
	for i in range(input_sz):
		if secret_code & (0x1<<i):
			fxckt.C(i,input_sz)
	# fxckt.draw()
	return fxckt

class bernvazi:
	def __init__(self, qsimsz):
		self.inputsz = qsimsz -1

	def gen_bv_ckt(self):
		print("Getting the secret function box...")
		fxckt = get_fxckt(self.inputsz+1) # returns FX that acts on self.inputsz + 1 qbits
		print("OK, FX is ready.")

		###########################################################################
		## Start of the Bernstien-Vazirani algorithm
		###########################################################################
		print()
		print("Starting the BV algorithm...")

		###########################################################################
		# Step 0: Prepare the result bit |b> to |->
		bv_ckt = qcckt.QCkt(self.inputsz+1)
		bv_ckt.X(self.inputsz)
		bv_ckt.H(self.inputsz)
		print("Step 0: Prepared |b> as |->")
		# bv_ckt.draw()

		###########################################################################
		## Step 1: Apply H on all qbits of |x>
		for i in range(self.inputsz):
			bv_ckt.H(i)
		print("Step 1: Applied H to all |x> qbits")
		# bv_ckt.draw()

		###########################################################################
		## Step 2: Now apply the secret function f()
		bv_ckt.Border()
		qbit_list = list(range(self.inputsz+1))
		# qbit_list.reverse()
		fxckt = fxckt.realign(self.inputsz+1,self.inputsz+1,qbit_list)
		bv_ckt = bv_ckt.append(fxckt)
		bv_ckt.Border()
		print("Step 2: Applied FX to |b>|x>")
		# bv_ckt.draw()

		###########################################################################
		## Step 3: Again apply H on all qbits of |x>
		for i in range(self.inputsz):
			bv_ckt.H(i)
		print("Step 3: Again Applied H to all |x> qbits")
		# bv_ckt.draw()

		###########################################################################
		## Step 4: Measure all qbits of |x>
		bv_ckt.M(list(range(self.inputsz))) # this will give [LSB, ..., MSB]
		print("Step 4: measure all |x> qbits")
		bv_ckt.draw()

		return bv_ckt


if __name__ == "__main__":
	# qc = qclib.qcsim(7)
	nqubits = 6
	bv = bernvazi(nqubits)
	bv_ckt = bv.gen_bv_ckt()
	bk = qcckt.Backend()
	bk.run(bv_ckt,qtrace=False)
	print(bk.get_creg())
