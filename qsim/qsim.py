#!/usr/bin/python3

# This file is part of the QSIM project covered under GPL v3 license.
# See the full license in the file LICENSE
# Author: Atul Varshneya

import numpy as np
import random as rnd
from copy import deepcopy
import types

## IMPORTANT: The qubit/clbit ordering convention is -- [MSB, ..., LSB]. Yes, :-), [0] is MSB.
##            NOTE: when refering to bits by position numbers, MSB would be 7, in an 8-qubit machine
##            So, CNOT 3,0 in an 8-qubit machine, woudld act on [ -, -, -, -, C, -, -, T], C=control, T = target
##            BUT, the state vector ordering is [0000, ...., 1111]. Good that it does not impact the user.
## Sorry, for this confusion, but too much effort to change now.

class QSimulator:

	def __init__(self, nq, ncbits=None, initstate=None, prepqubits=None, qtrace=False, qzeros=False, validation=False, visualize=False):
		# record input variables for reset
		self.nqbits = nq
		self.ncbits = ncbits
		if self.ncbits is None:
			self.ncbits = nq
		self.initstate = initstate
		self.prepqubits = prepqubits
		self.traceINP = qtrace
		self.disp_zerosINP = qzeros
		self.validation = validation
		self.visualize = visualize

		# Useful constants
		self.pi = np.pi
		self.errprec = 6 # number of digits after decimal
		self.maxerr = 10**(-self.errprec)
		self.probprec = 6 # number of digits after decimal
		self.maxproberr = 10**(-self.probprec)

		self.qreset()

	def qreset(self):
		# Reset the runtime Variables, in case qtraceON(), qzerosON() have changed them.
		self.trace = self.traceINP
		self.disp_zeros = self.disp_zerosINP

		# Clear the classical bits register
		self.cregister = [0]*self.ncbits

		# Initial State
		if not self.initstate is None:
			# check if the state is np.matrix type
			if not type(self.initstate) is np.matrixlib.defmatrix.matrix:
				errmsg = "User Error. Wrong type. Initstate must be a numpy.matrix."
				raise QSimError(errmsg)
			# check if the size of the passed state is 2**nqbits
			(rows,cols) = self.initstate.shape
			if rows != 2**self.nqbits or cols != 1:
				errmsg = "User Error. wrong dimensions. Initstate shape must be (2^nqbits,1)."
				raise QSimError(errmsg)
			# check if normalized
			p = 0
			for i in range(2**self.nqbits):
				p += np.absolute(self.initstate[i].item(0))**2
			if np.absolute(p-1.0) > self.maxerr:
				errmsg = "User Error. Initial state not normalized."
				raise QSimError(errmsg)
			self.sys_state = deepcopy(self.initstate)
		elif not self.prepqubits is None:
			if len(self.prepqubits) != self.nqbits:
				errmsg = "User Error. wrong dimensions. prepqubits has incorrect number of qbits."
				raise QSimError(errmsg)
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

	def qgate(self, oper, qbit_list, qtrace=False):
		##
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_qbit_list(qbit_list):
			errmsg = "Error: the list of qubits is not valid."
			raise QSimError(errmsg)
		if self.validation:
			if not self.qisunitary(oper):
				errmsg = "Error: Operator {:s} is not Unitary".format(oper[0])
				raise QSimError(errmsg)
		a_op = self.__stretched_mat(oper,qbit_list)
		self.sys_state = a_op * self.sys_state
		if qtrace or self.trace:
			opname = oper[0]
			opargs = str(qbit_list)
			hdr = opname + " Qubit" + opargs
			self.qreport(header=hdr)

	def qsnapshot(self):
		return self.cregister, self.sys_state

	def qmeasure(self, qbit_list, cbit_list=None, basis=None, qtrace=False):
		##
		if cbit_list is None:
			cbit_list = qbit_list
		## TODO: check cbit_list has all entries unique and within the cbit register
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_qbit_list(qbit_list):
			errmsg = "Error: the list of qubits is not valid."
			raise QSimError(errmsg)
		# check the validity of basis
		if (not basis is None) and self.validation:
			if not self.qisunitary(basis):
				errmsg = "Error: basis {:s} is not Unitary".format(basis[0])
				raise QSimError(errmsg)

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
			raise QSimError(errmsg)

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

		# finally update classical bits register with the measurement
		if len(qbit_list) != len(cbit_list):
			errmsg = "Error: list of classical bits is not valid"
			raise QSimError(errmsg)
		# print("meas_val = ", meas_val)
		# print("qbit_list = ", qbit_list)
		# print("cbit_list = ", cbit_list)
		for i in range(len(cbit_list)):
			self.cregister[self.nqbits - cbit_list[i]-1] = meas_val[i]

		if qtrace or self.trace:
			hdr = "MEASURED in basis "+bname+", Qubit" + str(qbit_list) + " = " + str(meas_val) + " with probability = " + str(round(prob_val,self.probprec-1)) 
			self.qreport(header=hdr)

		return meas_val


	def qreport(self, header="State", state=None, visualize=False):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		if state == None:
			state = self.sys_state
		print()
		print(header)
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
				print(ststr + ampstr + barstr)
		print("CREGISTER: ", end="")
		for i in range(self.ncbits): # cregister[0] is MSB
			print("{0:01b}".format(self.cregister[i]),end="")
		print()

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

	def SQSWAP(self):
		"""
		Swap gate.
		"""
		return ["SQSWAP", np.matrix([[1,0,0,0],[0,0.5+0.5j,0.5-0.5j,0],[0,0.5-0.5j,0.5+0.5j,0],[0,0,0,1]],dtype=complex)]

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

	def Hn(self,n):
		"""
		H^n gate - very commonly used
		"""
		op_list = []
		for i in range(n):
			op_list.append(self.H())
		return self.qcombine_par("H**{:d}".format(n),op_list)

	def RND(self):
		"""
		Random apmplitude gate.
		"""
		phi = rnd.random() * self.pi * 2
		camp = np.cos(phi)
		samp = np.sin(phi)
		phi = rnd.random() * self.pi * 2
		re1 = camp*np.cos(phi)
		im1 = camp*np.sin(phi)
		re2 = samp*np.cos(phi)
		im2 = samp*np.sin(phi)
		return ["RND", np.matrix([[complex(-re1,-im1),complex(re2,im2)],[complex(re2,im2),complex(re1,im1)]],dtype=complex)]

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
		return self.CTL(self.CTL(self.X()),name="TOFFOLI")

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

	## __aligned_op() and __stretched_mat() use two concepts core to
	## the working of this simulator.
	##
	## methods __qbit_realign_list(), __rmat_rrmat(), and __shuffled_count() are used
	## for the alignment of the operators as described below --
	##
	## Lets consider a 2-bit gate, e.g., CNOT gate, C, which, say, is defined
	## to take bit 1 as the control bit, and bit 0 as the target bit --
	##
	##         +---+
	## |b1> ---|-+-|------
	##         | | |
	## |b0> ---|-O-|------
	##         +---+
	##
	## Lets see how we apply this 2-qubit gate to some specifc bits of a 4 qubit system,
	## say, control qubit 3, and target qubit 1.
	## We first 'stretch' this to the full 4 qubits U = np.kron(np.eye(4), C). See below 
	## the description of __stretched_mat().
	##         +---+
	## |b3> ---|---|------
	##         |   |
	## |b2> ---|---|------
	##         |   |
	## |b1> ---| + |------
	##         | | |
	## |b0> ---| O |------
	##         +---+
	##           U
	## Note, U operator is a 2**nqbits x 2**nqbits matrix, 16x16 in this example case.
	## And note, that this will apply the operation to the qubits 0 and 1 as defined,
	## and leave the other qubits unchanged.
	## Remember, the operators act on a state vector to compute the resulting state 
	## vector, that is why the operator is 2**nqbits x 2**nqbits in size
	##
	## Next, we apply an operator, r, again a 2**nqbits x 2**nqbits matrix, on the state 
	## to reorder (realign) it such that the state vector is ordered counting with qubit 1 
	## at qbit 0 position, and qubit 3 at qubit 1 position. 
	## Next, apply U. Finally, apply an operator, rr, to undo the reordering done by 
	## the operator r.
	## So logically, the operators circuit diagram looks like -
	##         +---+  +---+  +---+
	## |b3> ---|  2|--|---|--|  3|----
	##         |   |  |   |  |   |
	## |b2> ---|  0|--|---|--|  2|----
	##         |   |  |   |  |   |
	## |b1> ---|  3|--| + |--|  1|----
	##         |   |  | | |  |   |
	## |b0> ---|  1|--| O |--|  0|----
	##         +---+  +---+  +---+
	##           r      U      rr
	## 
	## Now, if we multiple these three operators as a_op = (rr x U x r) then the resulting 
	## operator, calling it a_op, basically is the one that applies C on qubits 3 and 1 as intended.

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

	## __stretched_mat() and __aligned_op() use two concepts core to
	## the working of this simulator.
	##
	## Qubits |x> and |y>, each is acted upon by 2x2 operators U1 and U2, respectively.
	## This is equivalent to the combined state of x and y, i.e., |xy> acted upon
	## by a single 4x4 operator U = np.kron(U1, U2) (see Umesh Vazirani course
	## on edx.org - Week 3: Quantum Circuits and Teleportation  
	## Lecture 5: Quantum Gates  Video: Two Qubit Gates and Tensor Products
	## https://www.youtube.com/watch?v=ISJYwzN-W20 )
	##
	##            +-------+
	##            |       |
	##            | +---+ |
	##            | |   | |
	## |x> -------+-|U1 |-+-------- U1|x>                  +-----+
	##            | |2x2| |                                |     |
	##            | +---+ |                                |     |
	##            |       |                   |xy> --------+  U  +------- U|xy>
	##            |       |                                |     |
	##            | +---+ |                                | 4x4 |
	##            | |   | |                                +-----+
	## |y> -------+-|U1 |-+-------- U2|y>
	##            | |2x2| |
	##            | +---+ |
	##            |       |
	##            +-------+

	def __stretched_mat(self,oper,qbit_list):
		orignm = oper[0]
		op = oper[1]
		opargs = str(qbit_list)
		if (op.shape)[1] != (op.shape)[0]:
			errmsg = "Error. Operator is not a square matrix. "+orignm+"'s dimension = ("+str((op.shape)[0])+","+str((op.shape)[1])+")."
			raise QSimError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = "User Error. Wrong number of qbit args for operator "+orignm+". Provided arguments = "+opargs+"."
			raise QSimError(errmsg)
		c_op = np.kron(op,np.eye(2**(self.nqbits-len(qbit_list))))
		a_op = self.__aligned_op(c_op,qbit_list)
		return a_op

	def qstretch(self,oper,qbit_list):
		return ["{0:d}Q-{1:s}{2:s}".format(self.nqbits,oper[0],str(qbit_list)),self.__stretched_mat(oper,qbit_list)]

	def qcombine_seq(self,name,op_list):
		d = ((op_list[0])[1]).shape[0]
		res = np.matrix(np.eye(d),dtype=complex)
		for opdef in op_list:
			op = opdef[1]
			r = op.shape[0]
			c = op.shape[1]
			if r != c:
				errmsg = "Opearion is not a square matrix."
				raise QSimError(errmsg)
			if r != d:
				errmsg = "Opearion matrices not the same size."
				raise QSimError(errmsg)
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


class QSimError(BaseException):
	def __init__(self,arg):
		self.args = arg

if __name__ == "__main__":

	try:
		q = QSimulator(2,qtrace=True, visualize=True)
		q.qgate(q.H(),[1])
		q.qgate(q.C(), [1,0])

		quit()

		q = QSimulator(8,qtrace=True)

		print("Entangling 4 bits -------------------------")
		q.qgate(q.H(),[3])
		for i in range(3):
			q.qgate(q.CTL(),[3,i])
		print("-------------------------------------------")
		for i in range(4):
			q.qgate(q.X(),[i+4])
		q.qgate(q.Rphi(q.pi/2),[7])
		print("-------------------------------------------")
		v = q.qmeasure([2])
		print("Qubit 2 value measured = ",v)
		v = q.qmeasure([1])
		print("Qubit 1 value measured = ",v)
		q.qreport()
	except QSimError as m:
		print(m.args)

	# st = q.qstate()
	# for i in range(len(st)):
	#	print '{:08b}'.format(i), st[i]
