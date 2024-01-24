#!/usr/bin/env python

import qckt
import numpy as np
import random as rnd
from qckt import QCktException

#################################################################################
# Details @ https://en.wikipedia.org/wiki/Grover%27s_algorithm
#################################################################################

'''
This library 
'''

class Grover:
	def __init__(self, orcale_ckt, inpreg, outreg, nmarked=1, probestates=None):
		if len(outreg) != 1:
			errmsg = "Out register must have only 1 qubit"
			raise QCktException(errmsg)

		# first lookup the nqubits, nclbits in the circuit, and the input register size
		fullnqbits,fullncbits = orcale_ckt.get_size()
		inreg_len = len(inpreg)

		#### 1. Initialization circuit
		init_ckt = qckt.QCkt(fullnqbits,name="Initialize")
		init_ckt.H(inpreg)
		init_ckt.X(outreg)
		init_ckt.H(outreg)
		# init_ckt.draw()

		#### 2. Diffuser (amplifier) circuit
		amp_ckt = qckt.QCkt(fullnqbits, name="Diffuser")
		amp_ckt.H(inpreg)
		amp_ckt.X(inpreg)
		amp_ckt.CX(*(inpreg+outreg))
		amp_ckt.X(inpreg)
		amp_ckt.H(inpreg)
		# amp_ckt.draw()

		###
		# Now assemble the component circuits into the overall full circuit
		###
		fullckt = qckt.QCkt(fullnqbits,fullncbits,name="Full Grover's Circuit")
		#### 1. First add the init_ckt
		fullckt = fullckt.append(init_ckt)
		if probestates is not None:
			fullckt.Probe("after initialization",probestates=probestates)
		#### 2. now add the required number of oracle_ckt + amp_ckt pairs
		numitrs = int((np.pi/4.0) * ((2.0**(inreg_len))/nmarked)**0.5) # optimal # iter, less or more dont work
		# print("number of Invert-Diffuser iterations = ",numitrs)
		for itr in range(numitrs):
			fullckt = fullckt.append(orcale_ckt)
			fullckt = fullckt.append(amp_ckt)
			if probestates is not None:
				fullckt.Probe("after iteration "+str(itr+1), probestates=probestates)
		# fullckt.draw()
		self.groverckt = fullckt

	def getckt(self):
		return self.groverckt

if __name__ == "__main__":
	pass