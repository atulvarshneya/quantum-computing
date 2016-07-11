#!/usr/bin/python

import numpy as np
import random as rnd

class qclib:

	def __init__(self, nq, qtrace=False, qzeros=False):
		## System Variables
		self.nqbits = nq

		## Runtime Options
		self.trace = qtrace
		self.disp_zeros = qzeros

		## Convinience constants
		self.pi = np.pi

		## Initial State
		qbit = [None]*self.nqbits
		for i in range(self.nqbits):
			qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
		self.sys_state = qbit[self.nqbits-1]
		l = range(self.nqbits-1)
		l.reverse()
		for i in l:
			self.sys_state = np.kron(self.sys_state,qbit[i])
		if self.trace:
			self.qreport(header="Initial State")

	def shuffled_count(self, bitorder):
		sz = len(bitorder)
		shuffled = []
		for i in range(2**sz):
			shfval = 0
			for b in range(sz):
				dstbit = bitorder[sz-b-1]
				shfval += (((i >> b) & 0x1) << dstbit)
			shuffled.append(shfval)
		return shuffled

	def composite_op(self, op, opqbits):
		comp_op = op
		for i in range(self.nqbits-opqbits):
			comp_op = np.kron(comp_op,np.eye(2))
		return comp_op

	## qbit_reorder is 'visually correct'. So [a,b,c,d] implies MSB to be 
	## replaced by the bit in position 'a' in the original, next lower MSB 
	## to be replaced by bit in potion 'b' in the original, and so on ...
	def aligned_op(self, op, qbit_reorder):
		if self.nqbits != len(qbit_reorder):
			errmsg = "Internal Error. " + str(self.nqbits) + " qbit system. Alignment vector has incorrect size " + str(len(qbit_reorder))
			raise QClibError(errmsg)
		# this is the counting with the given bit ordering
		rr = self.shuffled_count(qbit_reorder)
		## create the rmat and rrmat
		imat = np.matrix(np.eye(2**self.nqbits))
		rmat = np.matrix(np.eye(2**self.nqbits))
		rrmat = np.matrix(np.eye(2**self.nqbits))
		for i in range(2**self.nqbits):
			s = rr[i]
			rmat[i] = imat[s]
			rrmat[s] = imat[i]
		a_op = rrmat * op * rmat
		return a_op

	def qbit_reorder_list(self, qbit_list):
		reord_list = qbit_list
		for i in range(self.nqbits):
			if i not in reord_list:
				reord_list.append(i)
		return reord_list

	def qgate(self, oper, qbit_list, display=False):
		opname = oper[0]
		opargs = str(qbit_list)
		op = oper[1]
		if (op.shape)[1] != (op.shape)[0]:
			errmsg = "Error. Operator is not a sqare matrix. Dimension = (",(op.shape)[0],",",(op.shape)[1],")."
			raise QClibError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = "User Error. Wrong number of qbit args for operator "+opname+". Provided arguments = "+opargs+"."
			raise QClibError(errmsg)
		c_op = self.composite_op(op,len(qbit_list))
		reord_list = self.qbit_reorder_list(qbit_list)
		a_op = self.aligned_op(c_op,reord_list)
		self.sys_state = a_op * self.sys_state
		if display or self.trace:
			hdr = opname + " Qbit" + opargs
			self.qreport(header=hdr)

	## not sure if this batch operation is any use, but threw it in anyways...
	def qgate_batch(self, op_arg_list, display=False):
		for o in op_arg_list:
			self.qgate(o[0],o[1],display=display)

	def qmeasure(self, qbit, display=False):
		bitmask = 0x1<<qbit
		amp_0 = 0
		amp_1 = 0
		meas_0_state = self.sys_state
		meas_1_state = self.sys_state
		for i in range(len(self.sys_state)):
			if (i & bitmask) == 0:
				amp_0 += np.absolute(self.sys_state[i].item(0))**2
			else:
				amp_1 += np.absolute(self.sys_state[i].item(0))**2
		toss = rnd.random()
		if toss <= amp_0:
			for i in range(len(self.sys_state)):
				if (i & bitmask) != 0:
					meas_0_state[i] = 0
			meas_0_state = meas_0_state / np.sqrt(amp_0)
			self.sys_state = meas_0_state
			qbit_val = 0
			prob = amp_0
		else:
			for i in range(len(self.sys_state)):
				if (i & bitmask) == 0:
					meas_1_state[i] = 0
			meas_1_state = meas_1_state / np.sqrt(amp_1)
			self.sys_state = meas_1_state
			qbit_val = 1
			prob = amp_1
		if display or self.trace:
			hdr = "MEASURED Qbit[" + str(qbit) + "] = " + str(qbit_val) + " with probality = " + str(prob) 
			self.qreport(header=hdr)

	def qreport(self, header="State", st=None):
		if st == None:
			st = self.sys_state
		print header
		for i in range(len(st)):
			if self.disp_zeros or np.absolute(st[i]) != 0:
				print format(i,'0'+str(self.nqbits)+'b')+"    "+"{:.8f}".format(np.around(st[i].item(0),8))
		print

	def qstate(self):
		state_array = np.squeeze(np.asarray(self.sys_state))
		return state_array
	def qsize(self):
		return self.nqbits

	def qtraceON(self, val):
		self.trace = val

	def qzerosON(self, val):
		self.disp_zeros = val

	## QC Gates
	def X(self):
		return ["PAULI_X", np.matrix([[0,1],[1,0]],dtype=complex)]
	def Y(self):
		return ["PAULI_Y", np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
	def Z(self):
		return ["PAULI_Z", np.matrix([[1,0],[0,-1]],dtype=complex)]
	def H(self):
		sqr2 = np.sqrt(2)
		return ["HADAMARD", np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)]
	def R(self,phi):
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		return ["R-PHI", np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)]
	def SWAP(self):
		return ["SWAP", np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)]
	def C(self):
		return ["C-NOT", np.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)]


class QClibError:
	def __init__(self,arg):
		self.args = arg

if __name__ == "__main__":
	q = qclib(8,qtrace=True)
	q.qtraceON(True)

	try:
		q.qgate(q.H(),[2])
		q.qgate(q.H(),[4])
		q.qgate(q.C(),[2,1])
		q.qgate(q.C(),[4,3])
		q.qtraceON(True)
		q.qmeasure(2)
		q.qmeasure(1)
		q.qreport()
	except QClibError, m:
		print m.args

	st = q.qstate()
	for i in range(len(st)):
		print '{:08b}'.format(i), st[i]
