#!/usr/bin/python

import numpy as np
import random as rnd
from copy import deepcopy
import types

class qcsim:

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
		self.maxerr = 0.000001
		self.maxproberr = 0.000001

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
				self.sys_state = np.kron(self.sys_state,qbit[i])
		if self.trace:
			self.qreport(header="Initial State")

	def qgate(self, oper, qbit_list, qtrace=False):
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
			hdr = opname + " Qbit" + opargs
			self.qreport(header=hdr)

	def qmeasure(self, qbit_list, basis=None, qtrace=False):
		##
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_qbit_list(qbit_list):
			errmsg = "Error: teh list of qubits is not valid."
			raise QClibError(errmsg)
		if (not basis is None) and self.validation:
			if not self.qisunitary(basis):
				errmsg = "Error: Operator {:s} is not Unitary".format(basis[0])
				raise QClibError(errmsg)
		bname = "STANDARD"
		if not basis is None:
			# first checck if basis provided is valid
			bname = basis[0]
			bmat = basis[1]
			(r,c) = bmat.shape
			if r != c:
				errmsg = "User Error. Provided basis is not a square matrix."
				raise QClibError(errmsg)
			isok = True
			trpbasis = np.transpose(bmat)
			pmat = np.asarray(np.dot(bmat,trpbasis))
			for i in range(r):
				for j in range(c):
					if i != j:
						if np.absolute(pmat[i][j]) > self.maxerr:
							isok = False
					else:
						if np.absolute(pmat[i][j]-1.0) > self.maxerr:
							isok = False
			if not isok:
				errmsg = "User Error. Provided basis does not have orthonormal vectors."
				raise QClibError(errmsg)

		# align the qbits to measure to the MSB
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
			hdr = "MEASURED in basis "+bname+", Qbit" + str(qbit_list) + " = " + str(meas_val) + " with probality = " + str(prob_val) 
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
					barstr = "x"
					amp = np.absolute(state[i].item(0))*barlen
					intamp = int(amp)
					if amp > self.maxerr:
						barstr = "|"
						for b in range(barlen):
							if b <= intamp:
								barstr = barstr+"*"
							else:
								barstr = barstr + "."
				ststr = ("{:0"+str(self.nqbits)+"b}    ").format(i)
				ampstr = "{:.8f}    ".format(np.around(state[i].item(0),8))
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

	## QC Gates
	def X(self):
		"""
		Pauli_X gate.
		"""
		return ["X", np.matrix([[0,1],[1,0]],dtype=complex)]
	def Y(self):
		"""
		Pauli_Y gate.
		"""
		return ["Y", np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
	def Z(self):
		"""
		Pauli_Z gate.
		"""
		return ["Z", np.matrix([[1,0],[0,-1]],dtype=complex)]
	def H(self):
		"""
		Hadamard gate.
		"""
		sqr2 = np.sqrt(2)
		return ["HADAMARD", np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)]
	def Rphi(self,phi):
		"""
		Phase rotation gate. Takes the Phi as an argument.
		"""
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		return ["ROTphi({:0.4f})".format(phi), np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)]
	def Rk(self,k):
		"""
		Controlled Phase rotation gate. Takes the k as an argument to divide 2*pi by 2**k.
		"""
		ck = np.cos(2*self.pi/(2**k))
		sk = np.sin(2*self.pi/(2**k))
		return ["ROTk({:d})".format(k), np.matrix([
			[1,0],
			[0,complex(ck,sk)]],dtype=complex)]
	def SWAP(self):
		"""
		Swap gate.
		"""
		return ["SWAP", np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)]

	def CSWAP(self):
		"""
		CSWAP gate
		"""
		return self.CTL(self.SWAP())

	def QFT(self,nqbits):
		N = 2**nqbits # number of rows and cols
		theta = 2.0 * np.pi / N
		opmat = [None]*N
		for i in range(N):
			# print "row",i,"--------------------"
			row = []
			for j in range(N):
				pow = i * j
				pow = pow % N
				# print "w^",pow
				row.append(np.e**(1.j*theta*pow))
			opmat[i] = row
		# print opmat
		opmat = np.matrix(opmat,dtype=complex) / np.sqrt(N)
		oper = ["QFT({:d})".format(nqbits),opmat]
		return oper

	def CTL(self,op,name=None):
		"""
		Add Control to any gate
		"""
		opname = op[0]
		opmat = op[1]
		(r,c) = opmat.shape
		oparr = np.array(opmat)
		coparr = np.eye(r*2,dtype=complex)
		for i in range(r,r*2):
			for j in range(r,r*2):
				coparr[i][j] = oparr[i-r][j-r]
		if name is None:
			name = "C"+opname
		return [name, np.matrix(coparr,dtype=complex)]

	def C(self):
		"""
		CNOT gate
		"""
		return self.CTL(self.X(),name="CNOT")

	def T(self):
		"""
		TOFFOLI gate.
		"""
		return self.CTL(self.CTL(self.X(),name="TOFFOLI"))

	# Basis Matrices
	def BELL_BASIS(self):
		return ["BELL_BASIS",np.matrix([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]], dtype=complex)/np.sqrt(2)]

	def HDM_BASIS(self):
		sq2 = np.sqrt(2)
		return ["HDM_BASIS",np.matrix([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)]



	####################################################################################################
	## Utility functions ###############################################################################
	####################################################################################################

	def __valid_qbit_list(self,qbit_list):
		if len(qbit_list) > self.nqbits:
			return False
		for i in qbit_list:
			if i >= self.nqbits:
				return False
			if qbit_list.count(i) != 1:
				return False
		return True

	def __shuffled_count(self, bitorder):
		sz = self.nqbits
		shuffled = []
		for i in range(2**sz):
			shfval = 0
			for b in range(sz):
				dstbit = bitorder[sz-b-1]
				shfval += (((i >> b) & 0x1) << dstbit)
			shuffled.append(shfval)
		return shuffled

	def __rmat_rrmat(self, qbit_reorder):
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
		return (rmat, rrmat)

	def __qbit_realign_list(self, qbit_list):
		reord_list = deepcopy(qbit_list)
		for i in reversed(range(self.nqbits)): # reversed to maintain significance order of the other qbits; poetic correctness :-)
			if i not in reord_list:
				reord_list.append(i)
		return reord_list

	def __aligned_op(self, op, qbit_list):
		"""
		qbit_reorder is 'visually correct'. So [a,b,c,d] implies bring to MSB 
		the bit in position 'a' in the original, brint to the next lower MSB 
		the bit in potion 'b' in the original, and so on ...
		"""
		qbit_reorder = self.__qbit_realign_list(qbit_list)
		(rmat,rrmat) = self.__rmat_rrmat(qbit_reorder)
		a_op = rrmat * op * rmat
		return a_op

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
		c_op = np.kron(op,np.eye(2**(self.nqbits-len(qbit_list))))
		a_op = self.__aligned_op(c_op,qbit_list)
		return a_op

	def qstretch(self,oper,qbit_list):
		return ["{:d}Q-{:s}{:s}".format(self.nqbits,oper[0],qbit_list),self.__stretched_mat(oper,qbit_list)]

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


class QClibError:
	def __init__(self,arg):
		self.args = arg

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
		print "Qbit 2 value measured = ",v
		v = q.qmeasure([1])
		print "Qbit 1 value measured = ",v
		q.qreport()
	except QClibError, m:
		print m.args

	# st = q.qstate()
	# for i in range(len(st)):
	#	print '{:08b}'.format(i), st[i]
