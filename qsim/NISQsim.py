#!/usr/bin/python3

# This file is part of the QSIM project covered under GPL v3 license.
# See the full license in the file LICENSE
# Author: Atul Varshneya

import numpy as np
import random as rnd
from copy import deepcopy
import types
from qSimException import QSimError

## IMPORTANT: The qubit/clbit ordering convention is -- [MSB, ..., LSB]. Yes, :-), [0] is MSB.
##            NOTE: when refering to bits by position numbers, MSB would be 7, in an 8-qubit machine
##            So, CNOT 3,0 in an 8-qubit machine, woudld act on [ -, -, -, -, C, -, -, T], C=control, T = target
##            BUT, the state vector ordering is [0000, ...., 1111]. Good that it does not impact the user.
## Sorry, for this confusion, but too much effort to change now.

class QSimulator:

	def __init__(self, nqbits, ncbits=None, initstate=None, prepqubits=None, qtrace=False, qzeros=False, verbose=False, validation=False, visualize=False):
		# record input variables for reset
		self.nqbits = nqbits
		self.ncbits = ncbits
		if self.ncbits is None:
			self.ncbits = nqbits
		self.initstate = initstate
		self.prepqubits = prepqubits
		self.sys_state = None
		self.traceINP = qtrace
		self.disp_zerosINP = qzeros
		self.verbose = verbose
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
		if self.disp_zeros:
			self.verbose = False # cannot print columns of sys density matrix if also displaying zeros

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
			# Now convert the state vector to density matrix
			self.sys_state = np.matrix(np.outer(self.sys_state, np.conjugate(self.sys_state)))
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
			# Now convert the state vector to density matrix
			self.sys_state = np.matrix(np.outer(self.sys_state, np.conjugate(self.sys_state)))
		else:
			# initialize the qbits to |0>
			qbit = [None]*self.nqbits
			for i in range(self.nqbits):
				qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
			# Now create the state as a tensor product of the qbits (MSB to the left)
			self.sys_state = qbit[self.nqbits-1]
			for i in reversed(range(self.nqbits-1)):
				self.sys_state = np.kron(qbit[i],self.sys_state)
			# Now convert the state vector to density matrix
			self.sys_state = np.matrix(np.outer(self.sys_state, np.conjugate(self.sys_state)))
		if self.trace:
			self.qreport(header="Initial State")

	def qgate(self, oper, qbit_list, qtrace=False):
		##
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_bit_list(qbit_list,self.nqbits):
			errmsg = "Error: the list of qubits is not valid."
			raise QSimError(errmsg)
		if self.validation:
			if not self.qisunitary(oper):
				errmsg = "Error: Operator {:s} is not Unitary".format(oper[0])
				raise QSimError(errmsg)
		a_op = self.__stretched_mat(oper,qbit_list)
		self.sys_state = a_op * self.sys_state * np.transpose(np.conjugate(a_op))
		if qtrace or self.trace:
			opname = oper[0]
			opargs = str(qbit_list)
			hdr = opname + " Qubit" + opargs
			self.qreport(header=hdr)

	def qsnapshot(self):
		return self.cregister, np.squeeze(np.asarray(self.sys_state))

	def qmeasure(self, qbit_list, cbit_list=None, qtrace=False):
		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits)
		if not self.__valid_bit_list(qbit_list,self.nqbits):
			errmsg = "Error: the list of qubits is not valid."
			raise QSimError(errmsg)

		if cbit_list is None:
			cbit_list = qbit_list
		# check the validity of the cbit_list (reapeated cbits, all cbits within self.ncbits)
		if not self.__valid_bit_list(cbit_list,self.ncbits):
			errmsg = "Error: the list of cubits is not valid."
			raise QSimError(errmsg)
		# check if equal number of qbits and cbits are passed
		if len(qbit_list) != len(cbit_list):
			errmsg = "Error: number of qbits and cbits passed are unequal."
			raise QSimError(errmsg)

		# align the qbits-to-measure to the MSB
		qbit_reorder = self.__qbit_realign_list(qbit_list)
		(rmat,rrmat) = self.__rmat_rrmat(qbit_reorder)
		# we have density amtrix, so alignment for rows as well as columns
		self.sys_state = rmat * self.sys_state
		self.sys_state = np.transpose(rmat * np.transpose(self.sys_state))

		list_len = len(qbit_list)
		qbitmask = 0
		for b in range(list_len):
			qbitmask |= 0x1 << (self.nqbits-b-1)
		shift_bits = self.nqbits - list_len

		# construct a M matrix for each possible value of qubits being measured.
		# E.g., if qbits 0,1 are being measured, create M00, M01, M02, M03.
		n_Mmats = 2**len(qbit_list)
		Mmats = [None] * n_Mmats
		prob = [0.0] * n_Mmats # later we will store the probabilities of each M observable
		for i in range(n_Mmats):
			Mmats[i] = np.matrix(np.zeros(self.sys_state.shape), dtype=complex)
		for i in range(2 ** self.nqbits):
			Mmat_idx = (i & qbitmask) >> shift_bits # Hmmm, could have kept the opposite bit order; too late now!!
			Mmats[Mmat_idx][i,i] = 1.0
		for i in range(n_Mmats):
			eta = Mmats[i] * self.sys_state * Mmats[i]
			prob[i] = np.trace(eta)

		# OK, now see which one should be selected
		toss = rnd.random()
		sel = len(prob) - 1 # to default if all the probs add up just short of 1, and toss == 1
		prob_val = prob[sel]
		cumprob = 0
		for i in range(len(prob)):
			if toss > cumprob and toss <= (cumprob + prob[i]):
				sel = i
			cumprob += prob[i]
		prob_val = np.absolute(prob[sel])
		meas_val = []
		for i in reversed(range(list_len)):
			if (sel & (0x1<<i)) == 0:
				meas_val.append(0)
			else:
				meas_val.append(1)

		# now, collapse to the selected state density matrix
		eta = Mmats[sel] * self.sys_state * Mmats[sel]
		self.sys_state = eta/prob_val

		# restore the alignment of sys_state
		self.sys_state = np.transpose(rrmat * np.transpose(self.sys_state))
		self.sys_state = rrmat * self.sys_state

		# finally update classical bits register with the measurement
		for i in range(len(cbit_list)):
			self.cregister[self.ncbits - cbit_list[i]-1] = meas_val[i]

		if qtrace or self.trace:
			hdr = "MEASURED "+"Qubit" + str(qbit_list) + " = " + str(meas_val) + " with probability = " + str(round(prob_val,self.probprec-1)) 
			self.qreport(header=hdr)

		return meas_val

	def qreport(self, header="State", state=None, probestates=None, visualize=False):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		if state is None:
			state = self.sys_state
		st_diag = np.diagonal(state)
		if probestates is not None:
			header = header + " - Probestates: "+str(probestates)
		print(header)

		if self.disp_zeros:
			self.verbose = False # cannot print columns of sys density matrix if also displaying zeros
		# identify rows and columns to print that are non-zero or disp_zeros is set
		(nrows,ncols) = state.shape
		pr_row = [False]*nrows
		pr_col = [False]*nrows
		for i in range(nrows):
			for j in range(ncols):
				if np.absolute(state[i,j]) > self.maxerr or self.disp_zeros:
					pr_row[i] = True
					pr_col[j] = True

		for i,row in enumerate(np.array(state)):
			if (probestates is None and pr_row[i]) or (probestates is not None and i in probestates):
				print(('{:0'+str(self.nqbits)+'b}    ').format(i), end='')
				if self.verbose:
					for j,v in enumerate(row):
						if (probestates is None and pr_col[j]) or (probestates is not None and j in probestates):
							print(f'{v:.2f} ', end='')
				else:
					print('...', end='')
				print(f' | {st_diag[i]:.4f}')
		purity = np.trace(self.sys_state * self.sys_state).real
		print(f'Mixed State Purity: {purity:.4f}')
		print("CREGISTER: ", end="")
		for i in range(self.ncbits): # cregister[0] is MSB
			print("{0:01b}".format(self.cregister[i]),end="")
		print()
		print()

	def qsize(self):
		return self.nqbits

	def qtraceON(self, val):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		self.trace = val

	def qzerosON(self, val):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		self.disp_zeros = val
		if self.disp_zeros:
			self.verbose = False # cannot print columns of sys density matrix if also displaying zeros


	####################################################################################################
	## Utility functions ###############################################################################
	####################################################################################################

	def __valid_bit_list(self,bit_list,nbits):
		if len(bit_list) > nbits:
			return False
		for i in bit_list:
			if i >= nbits:
				return False
			if bit_list.count(i) != 1:
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
		imat = np.array(np.eye(2**self.nqbits))
		rmat = np.array(np.eye(2**self.nqbits))
		rrmat = np.array(np.eye(2**self.nqbits))
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
	## say, control qubit 1, and target qubit 3.
	## We first 'stretch' this to the full 4 qubits U = np.kron(C, np.eye(4)). See below 
	## the description of __stretched_mat().
	##         +---+
	## |b3> ---|-+-|------
	##         | | |
	## |b2> ---|-O-|------
	##         |   |
	## |b1> ---|---|------
	##         |   |
	## |b0> ---|---|------
	##         +---+
	##           U
	## Note, U operator is a 2**nqbits x 2**nqbits matrix, 16x16 in this example case.
	## And note, that this will apply the operation to the qubits 3 (control) and 2 (target) i.e., 
	## most-significant qubits, and leave the other qubits unchanged.
	##
	## Remember, operators act on a state vector to compute the resulting state 
	## vector, that is why the operator is 2**nqbits x 2**nqbits in size
	##
	## Next, we apply an operator, r, a 2**nqbits x 2**nqbits matrix, on the state 
	## to reorder (realign) it such that the state vector is ordered counting with qubit 1 
	## at qubit 3 position, and qubit 3 at qubit 2 position. 
	## Next, apply U. Finally, apply an operator, rr, to undo the reordering done by 
	## the operator r.
	## So logically, the operators circuit diagram looks like -
	##         +---+  +---+  +---+
	## |b3> ---|3 1|--|-+-|--|1 3|----
	##         |   |  | | |  |   |
	## |b2> ---|2 3|--|-O-|--|3 2|----
	##         |   |  |   |  |   |
	## |b1> ---|1 2|--|---|--|2 1|----
	##         |   |  |   |  |   |
	## |b0> ---|0 0|--|---|--|0 0|----
	##         +---+  +---+  +---+
	##           r      U      rr
	## 
	## Now, if we multiple these three operators as a_op = (rr x U x r) then the resulting 
	## operator, calling it a_op, basically is the one that applies C on qubits 1 and 3 as intended.

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

	def qinverse(self,op,name=None):
		if name is None:
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


if __name__ == "__main__":

	import qgates as qgt
	try:
		q = QSimulator(3,qtrace=True, verbose=True)
		q.qgate(qgt.H(),[2])
		q.qgate(qgt.C(),[2,1])
		# q.qgate(qgt.H(),[1])
		q.qreport('Final state')
		q.qzerosON(True)
		q.qmeasure([2,1])
		# q.densmat_realign_test([0])

		quit()

		q = QSimulator(4,qtrace=True)

		print("Entangling 2 bits -------------------------")
		q.qgate(qgt.H(),[1])
		for i in range(1):
			q.qgate(qgt.C(),[1,i])
		print("-------------------------------------------")
		for i in range(1):
			q.qgate(qgt.X(),[i+2])
		# q.qgate(qgt.Rphi(q.pi/2),[7])
		print("-------------------------------------------")
		# v = q.qmeasure([2])
		# print("Qubit 2 value measured = ",v)
		# v = q.qmeasure([1])
		# print("Qubit 1 value measured = ",v)
		# q.qreport()
	except QSimError as m:
		print(m.args)
