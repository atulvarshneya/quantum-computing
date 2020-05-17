#!/usr/bin/python3

# This file is part of the QCLIB project covered under GPL v3 license.
# See the full license in the file LICENSE
# Author: Atul Varshneya

import numpy as np
import random as rnd
from copy import deepcopy
import types

from qcerror import *
import qcutilsgts as ugts
import qcutilsckt as uckt

class QCSim:

	def __init__(self, nq, initstate=None, prepqubits=None, qtrace=False, qzeros=False, validation=False, visualize=False):
		# record input variables for reset
		self.nqbits = nq
		self.initstate = initstate
		self.prepqubits = prepqubits
		self.traceINP = qtrace
		self.disp_zerosINP = qzeros
		self.validation = validation
		self.visualize = visualize

		# Useful constants
		self.pi = np.pi

		self.qreset()

	def qreset(self):
		# Reset the runtime Variables, in case qtraceON(), qzerosON() have changed them.
		self.trace = self.traceINP
		self.disp_zeros = self.disp_zerosINP

		# Initial State
		if not self.initstate is None:
			# check if the state is np.matrix type
			if not type(self.initstate) is np.matrixlib.defmatrix.matrix:
				errmsg = "User Error. Wrong type. Initstate must be a numpy.matrix."
				raise QClibError(errmsg)
			# check if the size of the passed state is 2**nqbits
			(rows,cols) = self.initstate.shape
			if rows != 2**self.nqbits or cols != 1:
				errmsg = "User Error. wrong dimensions. Initstate shape must be (2^nqbits,1)."
				raise QClibError(errmsg)
			# check if normalized
			p = 0
			for i in range(2**self.nqbits):
				p += np.absolute(self.initstate[i].item(0))**2
			if np.absolute(p-1.0) > self.maxerr:
				errmsg = "User Error. Initial state not normalized."
				raise QClibError(errmsg)
			self.sys_state = deepcopy(self.initstate)
		elif not self.prepqubits is None:
			if len(self.prepqubits) != self.nqbits:
				errmsg = "User Error. wrong dimensions. prepqubits has incorrect number of qbits."
				raise QClibError(errmsg)
			pqbit = np.transpose(np.matrix(self.prepqubits[self.nqbits-1],dtype=complex))
			prepstate = pqbit
			for i in reversed(range(self.nqbits-1)):
				pqbit = np.transpose(np.matrix(self.prepqubits[i],dtype=complex))
				prepstate = np.kron(pqbit,prepstate)
			p = 0
			for i in range(len(prepstate)):
				p += np.absolute(prepstate[i].item(0))**2
			prepstate = prepstate/np.sqrt(p)
			self.sys_state = prepstate
		else:
			# initialize the qbits to |0>
			qbit = [None]*self.nqbits
			for i in range(self.nqbits):
				qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
			# Now create the state as a tensor product of the qbits (MSB to the left)
			self.sys_state = qbit[self.nqbits-1]
			for i in reversed(range(self.nqbits-1)):
				self.sys_state = np.kron(qbit[i],self.sys_state)
		if self.trace:
			self.qreport(header="Initial State")

	def exec_qgate(self, oper, qbit_list, qtrace=False):
		##
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_qbit_list(qbit_list):
			errmsg = "Error: the list of qubits is not valid."
			raise QClibError(errmsg)
		if self.validation:
			if not self.qisunitary(oper):
				errmsg = "Error: Operator {:s} is not Unitary".format(oper[0])
				raise QClibError(errmsg)
		a_op = self.__stretched_mat(oper,qbit_list)
		self.sys_state = a_op * self.sys_state
		if qtrace or self.trace:
			opname = oper[0]
			opargs = str(qbit_list)
			hdr = opname + " Qubit" + opargs
			self.qreport(header=hdr)

	def exec_qmeasure(self, qbit_list, basis=None, qtrace=False):
		##
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_qbit_list(qbit_list):
			errmsg = "Error: teh list of qubits is not valid."
			raise QClibError(errmsg)
		# check the validity of basis
		if (not basis is None) and self.validation:
			if not self.qisunitary(basis):
				errmsg = "Error: basis {:s} is not Unitary".format(basis[0])
				raise QClibError(errmsg)

		# pick out the name and, if available, the matrix of this basis
		bname = "STANDARD"
		if not basis is None:
			bname = basis[0]
			bmat = basis[1]

		# align the qbits-to-measure to the MSB
		qbit_reorder = self.__qbit_realign_list(qbit_list)
		(rmat,rrmat) = self.__rmat_rrmat(qbit_reorder)
		self.sys_state = rmat * self.sys_state

		# align with basis
		if not basis is None:
			# Convert the mentioned qbits in the state to the given basis
			full_sz_basis_mat = np.kron(bmat, np.eye(2**(self.nqbits-len(qbit_list))))
			self.sys_state = full_sz_basis_mat * self.sys_state

		list_len = len(qbit_list)
		qbitmask = 0
		for b in range(list_len):
			qbitmask |= 0x1 << (self.nqbits-b-1)
		shift_bits = self.nqbits - list_len

		# add up the probability of the various combinations of the qbits to measure
		prob = [0]*(2**list_len)
		for i in range(len(self.sys_state)):
			prob_idx = (i & qbitmask) >> shift_bits # Hmmm, could have kept the opposite bit order; too late now!!
			prob[prob_idx] += np.absolute(self.sys_state[i].item(0))**2
		# ... and verify the total probability adds up to 1.0, within the acceptable margin
		totprob = 0
		for p in prob:
			totprob += p
		if np.absolute(totprob - 1.0) > self.maxproberr:
			errmsg = "Internal error, total probability != 1  (total prob = {:f}".format(totprob)
			raise QClibError(errmsg)

		# OK, now see which one should be selected
		toss = rnd.random()
		sel = len(prob) - 1 # to default if all the probs add up just short of 1, and toss == 1
		prob_val = prob[sel]
		cumprob = 0
		for i in range(len(prob)):
			if toss > cumprob and toss <= (cumprob + prob[i]):
				sel = i
			cumprob += prob[i]
		prob_val = prob[sel]
		meas_val = []
		for i in reversed(range(list_len)):
			if (sel & (0x1<<i)) == 0:
				meas_val.append(0)
			else:
				meas_val.append(1)

		# now, collapse to the selected state (all other amplitudes = 0, and normlize the amplitudes
		to_match = sel << shift_bits
		for i in range(len(self.sys_state)):
			if (i & qbitmask) == to_match:
				self.sys_state[i] = self.sys_state[i] / np.sqrt(prob_val)
			else:
				self.sys_state[i] = 0

		# align back with standard basis
		if not basis is None:
			# Convert the mentioned qbits in the state to the given basis
			invbasis = np.conjugate(np.transpose(bmat))
			full_sz_invbasis_mat = np.kron(invbasis, np.eye(2**(self.nqbits-len(qbit_list))))
			self.sys_state = full_sz_invbasis_mat * self.sys_state

		# align the qbits back to original
		self.sys_state = rrmat * self.sys_state

		if qtrace or self.trace:
			hdr = "MEASURED in basis "+bname+", Qubit" + str(qbit_list) + " = " + str(meas_val) + " with probability = " + str(prob_val) 
			self.qreport(header=hdr)
		return meas_val

	def qreport(self, header="State", state=None, visualize=False):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		if state == None:
			state = self.sys_state
		print
		print header
		for i in range(len(state)):
			if self.disp_zeros or np.absolute(state[i]) > self.maxerr:
				barlen = 20
				barstr = ""
				if self.visualize or visualize:
					barstr = "	x"
					amp = np.absolute(state[i].item(0))*barlen
					intamp = int(amp)
					if amp > self.maxerr:
						barstr = "	|"
						for b in range(barlen):
							if b <= intamp:
								barstr = barstr+"*"
							else:
								barstr = barstr + "."
				ststr = ("{:0"+str(self.nqbits)+"b}    ").format(i)
				ampstr = "{:.8f}".format(np.around(state[i].item(0),8))
				print ststr + ampstr + barstr

	def qstate(self):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		state_array = np.squeeze(np.asarray(self.sys_state))
		return state_array

	def qsize(self):
		return self.nqbits

	def qtraceON(self, val):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		self.trace = val

	def qzerosON(self, val):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		self.disp_zeros = val

if __name__ == "__main__":

	try:
		q = qcsim(2,qtrace=True, visualize=True)
		q.qgate(q.H(),[1])
		q.qgate(q.C(), [1,0])

		quit()

		q = qcsim(8,qtrace=True)

		print "Entangling 4 bits -------------------------"
		q.qgate(q.H(),[3])
		for i in range(3):
			q.qgate(q.CTL(),[3,i])
		print "-------------------------------------------"
		for i in range(4):
			q.qgate(q.X(),[i+4])
		q.qgate(q.Rphi(q.pi/2),[7])
		print "-------------------------------------------"
		v = q.qmeasure([2])
		print "Qubit 2 value measured = ",v
		v = q.qmeasure([1])
		print "Qubit 1 value measured = ",v
		q.qreport()
	except QClibError, m:
		print m.args

	# st = q.qstate()
	# for i in range(len(st)):
	#	print '{:08b}'.format(i), st[i]
