#!/usr/bin/python

import numpy as np
import random as rnd
from copy import deepcopy
import types

class qcsim:

	def __init__(self, nq, prepare=None, qtrace=False, qzeros=False):
		# System Variables
		self.nqbits = nq

		# Runtime Options
		self.trace = qtrace
		self.disp_zeros = qzeros

		# Useful constants
		self.pi = np.pi
		self.maxerr = 0.000001

		# Initial State
		# Check the validity of the 'prepared' state passed
		preplen = 0
		if not prepare is None:
			# if prepare id provided, check its sanity first
			if not type(prepare) is np.matrixlib.defmatrix.matrix:
				errmsg = "User Error. Wrong type. Prepared qbits not a numpy.matrix."
				raise QClibError(errmsg)
			(preplen,w) = prepare.shape
			if w != 2:
				errmsg = "User Error. wrong dimensions. Prepared qbits shape not (n,2)."
				raise QClibError(errmsg)
			if preplen > self.nqbits:
				errmsg = "User Error. Parameter 'prepare' has too many qbits."
				raise QClibError(errmsg)
		prepqb = np.asarray(prepare)
		for qb in prepqb:
			qbmag = np.sqrt(np.absolute(qb[0])**2 + np.absolute(qb[1])**2)
			if np.absolute(qbmag - 1) > self.maxerr:
				errmsg = "User Error. Parameter 'prepare' qbit not normalized."
				raise QClibError(errmsg)
		offst = self.nqbits - preplen
		# initialize the qbits
		qbit = [None]*self.nqbits
		for i in range(self.nqbits):
			if i >= offst:
				qbit[i] = np.transpose(np.matrix(prepqb[self.nqbits-i-1],dtype=complex))
			else:
				qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
		# Now create the state as a tensor product of the qbits (MSB to the left)
		self.sys_state = qbit[self.nqbits-1]
		l = range(self.nqbits-1)
		l.reverse()
		for i in l:
			self.sys_state = np.kron(self.sys_state,qbit[i])
		if self.trace:
			self.qreport(header="Initial State")

	def __shuffled_count(self, bitorder):
		sz = len(bitorder)
		shuffled = []
		for i in range(2**sz):
			shfval = 0
			for b in range(sz):
				dstbit = bitorder[sz-b-1]
				shfval += (((i >> b) & 0x1) << dstbit)
			shuffled.append(shfval)
		return shuffled

	def __resize_opmatrix(self, op):
		comp_op = deepcopy(op)
		opqbits = int(np.log2(op.shape[0]))
		for i in range(self.nqbits-opqbits):
			comp_op = np.kron(comp_op,np.eye(2))
		return comp_op

	def __aligned_op(self, op, qbit_reorder):
		"""
		qbit_reorder is 'visually correct'. So [a,b,c,d] implies MSB to be 
		replaced by the bit in position 'a' in the original, next lower MSB 
		to be replaced by bit in potion 'b' in the original, and so on ...
		"""
		if self.nqbits != len(qbit_reorder):
			errmsg = "Internal Error. " + str(self.nqbits) + " qbit system. Alignment vector has incorrect size " + str(len(qbit_reorder))
			raise QClibError(errmsg)
		# this is the counting with the given bit ordering
		rr = self.__shuffled_count(qbit_reorder)
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

	def __qbit_realign_list(self, qbit_list):
		reord_list = deepcopy(qbit_list)
		for i in range(self.nqbits):
			if i not in reord_list:
				reord_list.append(i)
		return reord_list

	def __stretched_mat(self,oper,qbit_list):
		orignm = oper[0]
		op = oper[1]
		opargs = str(qbit_list)
		if (op.shape)[1] != (op.shape)[0]:
			errmsg = "Error. Operator is not a square matrix. "+orignm+"'s dimension = ("+str((op.shape)[0])+","+str((op.shape)[1])+")."
			raise QClibError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = "User Error. Wrong number of qbit args for operator "+orignm+". Provided arguments = "+opargs+"."
			raise QClibError(errmsg)
		c_op = self.__resize_opmatrix(op)
		reord_list = self.__qbit_realign_list(qbit_list)
		a_op = self.__aligned_op(c_op,reord_list)
		return a_op

	def qstretch(self,oper,qbit_list):
		return ["{:d}Q-{:s}{:s}".format(self.nqbits,oper[0],qbit_list),self.__stretched_mat(oper,qbit_list)]

	def qgate(self, oper, qbit_list, display=False):
		a_op = self.__stretched_mat(oper,qbit_list)
		self.sys_state = a_op * self.sys_state
		if display or self.trace:
			opname = oper[0]
			opargs = str(qbit_list)
			hdr = opname + " Qbit" + opargs
			self.qreport(header=hdr)

	def qgate_batch(self, op_arg_list, display=False):
		"""
		Not sure if this batch operation is of any use, but threw it in anyways...
		"""
		for o in op_arg_list:
			self.qgate(o[0],o[1],display=display)

	def qcombine_seq(self,name,op_list):
		d = ((op_list[0])[1]).shape[0]
		res = np.matrix(np.eye(d),dtype=complex)
		for opdef in op_list:
			op = opdef[1]
			r = op.shape[0]
			c = op.shape[1]
			if r != c:
				errmsg = "Opearion is not a square matrix."
				raise QClibError(errmsg)
			if r != d:
				errmsg = "Opearion matrices not the same size."
				raise QClibError(errmsg)
			res = op*res # remember order of multiplication is opposite of the visual order
		return [name,res]

	def qcombine_par(self,name,op_list):
		res = None
		first = True
		for op in op_list:
			mat = op[1]
			if first:
				res = mat
				first = False
			else:
				res = np.kron(res,mat)
		return [name,res]

	def qinverse(self,op,name=None):
		if name == None:
			name = "INV-"+op[0]
		mat = deepcopy(op[1])
		invmat = np.conjugate(np.transpose(mat))
		return [name,invmat]

	def qisunitary(self,op):
		mat = op[1]
		(r,c) = mat.shape
		if r != c:
			return False
		invmat = np.conjugate(np.transpose(mat))
		pmat = np.asarray(mat * invmat)
		for i in range(r):
			for j in range(c):
				if i != j:
					if np.absolute(pmat[i][j]) > self.maxerr:
						return False
				else:
					if np.absolute(pmat[i][j]-1.0) > self.maxerr:
						return False
		return True

	def qmeasure(self, qbit, basis=None, display=False):
		bitmask = 0x1<<qbit
		prob_0 = 0
		prob_1 = 0
		for i in range(len(self.sys_state)):
			if (i & bitmask) == 0:
				prob_0 += np.absolute(self.sys_state[i].item(0))**2
			else:
				prob_1 += np.absolute(self.sys_state[i].item(0))**2
		if np.absolute((prob_0 + prob_1) - 1.0) > 0.000001:
			errmsg = "Internal error, amplitudes ( {:0.4f} and {:0.4f} ) do not add to probability = 1.".format(prob_0,prob_1)
			raise QClibError(errmsg)
		toss = rnd.random()
		# should round toss to 6 decimal places to align with the error check above (error < 0.000001)
		if toss <= prob_0:
			for i in range(len(self.sys_state)):
				if (i & bitmask) != 0:
					self.sys_state[i] = 0
			self.sys_state = self.sys_state / np.sqrt(prob_0)
			qbit_val = 0
			prob = prob_0
		else: # toss > prob_0
			for i in range(len(self.sys_state)):
				if (i & bitmask) == 0:
					self.sys_state[i] = 0
			self.sys_state = self.sys_state / np.sqrt(prob_1)
			qbit_val = 1
			prob = prob_1
		if display or self.trace:
			hdr = "MEASURED Qbit[" + str(qbit) + "] = " + str(qbit_val) + " with probality = " + str(prob) 
			self.qreport(header=hdr)
		return qbit_val

	def qreport(self, header="State", state=None):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		if state == None:
			state = self.sys_state
		print
		print header
		for i in range(len(state)):
			if self.disp_zeros or np.absolute(state[i]) != 0:
				print format(i,'0'+str(self.nqbits)+'b')+"    "+"{:.8f}".format(np.around(state[i].item(0),8))

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

	## QC Gates
	def X(self):
		"""
		Pauli_X gate.
		"""
		return ["PAULI_X", np.matrix([[0,1],[1,0]],dtype=complex)]
	def Y(self):
		"""
		Pauli_Y gate.
		"""
		return ["PAULI_Y", np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
	def Z(self):
		"""
		Pauli_Z gate.
		"""
		return ["PAULI_Z", np.matrix([[1,0],[0,-1]],dtype=complex)]
	def H(self):
		"""
		Hadamard gate.
		"""
		sqr2 = np.sqrt(2)
		return ["HADAMARD", np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)]
	def R(self,phi):
		"""
		Phase rotation gate. Takes the Phi as an argument.
		"""
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		return ["PHASE-ROT({:0.4f})".format(phi), np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)]
	def SWAP(self):
		"""
		Swap gate.
		"""
		return ["SWAP", np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)]
	def C(self):
		"""
		Controlled NOT gate.
		"""
		return ["C-NOT", np.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)]

	# Basis Matrices
	def BELL_BASIS(self):
		return np.matrix([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]], dtype=complex)


class QClibError:
	def __init__(self,arg):
		self.args = arg

if __name__ == "__main__":
	q = qcsim(8,qtrace=True)

	try:
		print "Entangling 4 bits -------------------------"
		q.qgate(q.H(),[3])
		for i in range(3):
			q.qgate(q.C(),[3,i])
		print "-------------------------------------------"
		for i in range(4):
			q.qgate(q.X(),[i+4])
		q.qgate(q.R(q.pi/2),[7])
		print "-------------------------------------------"
		v = q.qmeasure(2)
		print "Qbit 2 value measured = ",v
		v = q.qmeasure(1)
		print "Qbit 1 value measured = ",v
		q.qreport()
	except QClibError, m:
		print m.args

	# st = q.qstate()
	# for i in range(len(st)):
	#	print '{:08b}'.format(i), st[i]
