#!/usr/bin/env python

import qsim
import qgates as qgt
import qgatesUtils as qgu

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
def get_fx(qc):
	input_sz = qc.qsize() - 1
	secret_code = 0b11101
	code_fmt = "{:0"+"{:d}".format(input_sz)+"b}"
	print("Pssst... the secret code is ",code_fmt.format(secret_code))
	fx_oplist = []
	for i in range(input_sz):
		if secret_code & (0x1<<i):
			sn_optep = qc.qstretch(qgt.C(),[i,input_sz])
			fx_oplist.append(sn_optep)
	fx = qgu.qcombine_seq("FX",fx_oplist)
	return fx

class bernvazi:
	def __init__(self,qc):
		self.qc = qc
		self.inputsz = self.qc.qsize() -1

	def run(self):
		code_fmt = "{:0"+"{:d}".format(self.inputsz)+"b}"
		print("Getting the secret function box...")
		fx = get_fx(self.qc) # returns FX that acts on self.inputsz + 1 qbits
		print("OK, FX is ready.")

		###########################################################################
		## Start of the Bernstien-Vazirani algorithm
		###########################################################################
		print()
		print("Starting the BV algorithm...")

		###########################################################################
		# Step 0: Prepare the result bit |b> to |->
		self.qc.qgate(qgt.X(),[self.inputsz])
		self.qc.qgate(qgt.H(),[self.inputsz])
		print("Step 0: Prepared |b> as |->")

		###########################################################################
		## Step 1: Apply H on all qbits of |x>
		for i in range(self.inputsz):
			self.qc.qgate(qgt.H(),[i])
		print("Step 1: Applied H to all |x> qbits")

		###########################################################################
		## Step 2: Now apply the secret function f()
		qbit_list = list(range(self.inputsz+1))
		qbit_list.reverse()
		self.qc.qgate(fx,qbit_list)
		print("Step 2: Applied FX to |b>|x>")

		###########################################################################
		## Step 3: Again apply H on all qbits of |x>
		for i in range(self.inputsz):
			self.qc.qgate(qgt.H(),[i])
		print("Step 3: Again Applied H to all |x> qbits")

		###########################################################################
		## Step 4: Measure all qbits of |x>
		v = self.qc.qmeasure(list(range(self.inputsz))) # this will give [LSB, ..., MSB]
		res = 0
		for i in range(self.inputsz):
			res += (v[i] << i)
		print("Step 4: Measured all qbits of |x>")

		print("Result = "+code_fmt.format(res))

if __name__ == "__main__":
	qc = qsim.QSimulator(7)
	bv = bernvazi(qc)
	bv.run()
