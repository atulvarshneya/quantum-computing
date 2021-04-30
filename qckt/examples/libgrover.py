#!/usr/bin/python3

import qckt
import Registers as regs
import numpy as np
import random as rnd
from qException import QCktException

#################################################################################
# Details @ https://en.wikipedia.org/wiki/Grover%27s_algorithm
#################################################################################

class Grover:
	def __init__(self, uf_ckt, qinreg, qoutreg, nmarked=1,probestates=None):
		if len(qoutreg) != 1:
			errmsg = "Out register must have only 1 qubit"
			raise QCktException(errmsg)

		# first just stash away all the arguments passed on here
		self.uf_ckt = uf_ckt
		self.uf_inreg = qinreg
		self.uf_outreg = qoutreg
		self.nmarked = nmarked
		self.probestates = probestates
		self.fullnqbits,self.fullncbits = uf_ckt.get_size()
		self.groverckt = None

		# compute the sizes of the in,out and the overall circuit
		inreg_len = len(self.uf_inreg)
		outreg_len = len(self.uf_outreg)

		###
		# Start building the basic grover circuit, sized appropritely for the in and out registers
		###
		self.compact_inreg  = regs.QRegister(inreg_len)
		self.compact_outreg = regs.QRegister(outreg_len)
		totreg_len,_,_,_ = regs.placement(self.compact_outreg,self.compact_inreg)

		#### 1. Initialization circuit
		init_ckt = qckt.QCkt(totreg_len,name="Initialize")
		#### 1.1 all inreg haramard'ed
		init_ckt.H(self.compact_inreg)
		#### 1.2 setup the outreg qubit in |-> state for phase kickback
		init_ckt.X(self.compact_outreg)
		init_ckt.H(self.compact_outreg)
		init_ckt.Border()
		# init_ckt.draw()

		#### 2. Diffuser (amplifier) circuit
		amp_ckt = qckt.QCkt(totreg_len, name="Diffuser")
		#### 2.1 all inreg hadanard'ed and X'ed; basically an inverter circuit for key = |00...0>
		amp_ckt.H(self.compact_inreg)
		amp_ckt.X(self.compact_inreg)
		#### 2.2 perform out-qubit (X) inreg
		amp_ckt.CX(*(self.compact_inreg+self.compact_outreg))   ## This is how Umesh Vazirni explains it
		# amp_ckt.CZ(*(self.compact_inreg+self.compact_outreg)) ## Gives identical results ... since still invertig phase of the inputs register.
		#### 2.3 undo X and hadamard on all inreg qubits
		amp_ckt.X(self.compact_inreg)
		amp_ckt.H(self.compact_inreg)
		# amp_ckt.draw()

		###
		# Now assemble all the componet circuits into the overall full circuit
		###
		fullckt = qckt.QCkt(self.fullnqbits,self.fullncbits,name="Full Grover's Circuit")
		#### 1. align init_ckt and amp_ckt to the actual qubits assigned in the provided uf_ckt
		init_ckt = init_ckt.realign(self.fullnqbits,self.fullncbits,self.uf_outreg+self.uf_inreg)
		amp_ckt = amp_ckt.realign(self.fullnqbits,self.fullncbits,self.uf_outreg+self.uf_inreg)
		#### 2.1 First add the init_ckt
		fullckt = fullckt.append(init_ckt)
		if self.probestates is not None:
			fullckt.Probe("after initialization",probestates=self.probestates)
		#### 2.2 now add the required number of uf_ckt + amp_ckt pairs
		numitrs = int((np.pi/4.0) * ((2.0**(inreg_len))/nmarked)**0.5) # optimal # iter, less or more dont work
		# print("number of Invert-Diffuser iterations = ",numitrs)
		for itr in range(numitrs):
			fullckt = fullckt.append(uf_ckt)
			fullckt = fullckt.append(amp_ckt)
			if self.probestates is not None:
				fullckt.Probe("after iteration "+str(itr+1), probestates=self.probestates)
			fullckt.Border()
		# print("### Grover's Circuit ################################")
		# fullckt.draw()
		self.groverckt = fullckt

	def getckt(self):
		return self.groverckt

if __name__ == "__main__":

	pass
