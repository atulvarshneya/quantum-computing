
import numpy as np
from qcerror import *
import qcutilsgts as ugts

maxerr = 0.000001
maxproberr = 0.000001

class QCUtilsCkt:

	def __init__(self, nq):
		self.nqubits = nq

	####################################################################################################
	## Utility functions ###############################################################################
	####################################################################################################

	def valid_qbit_list(self,qbit_list):
		for i in qbit_list:
			if i >= self.nqubits:
				return False
			if qbit_list.count(i) != 1:
				return False
		return True

	def __shuffled_count(self, bitorder):
		sz = self.nqubits
		shuffled = []
		for i in range(2**sz):
			shfval = 0
			for b in range(sz):
				dstbit = bitorder[sz-b-1]
				shfval += (((i >> b) & 0x1) << dstbit)
			shuffled.append(shfval)
		return shuffled

	def __qbit_realign_list(self, qbit_list):
		reord_list = deepcopy(qbit_list)
		for i in reversed(range(self.nqubits)): # reversed to maintain significance order of the other qbits; poetic correctness :-)
			if i not in reord_list:
				reord_list.append(i)
		return reord_list

	def __rmat_rrmat(self, qbit_reorder):
		# this is the counting with the given bit ordering
		rr = self.__shuffled_count(qbit_reorder)
		## create the rmat and rrmat
		imat = np.matrix(np.eye(2**self.nqubits))
		rmat = np.matrix(np.eye(2**self.nqubits))
		rrmat = np.matrix(np.eye(2**self.nqubits))
		for i in range(2**self.nqubits):
			s = rr[i]
			rmat[i] = imat[s]
			rrmat[s] = imat[i]
		return (rmat, rrmat)

	## __aligned_op() and qstretch() use two concepts core to
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
	## the description of qstretch().
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
	## Note, U operator is a 2**nqubits x 2**nqubits matrix, 16x16 in this example case.
	## And note, that this will apply the operation to the qubits 0 and 1 as defined,
	## and leave the other qubits unchanged.
	## Remember, the operators act on a state vector to compute the resulting state 
	## vector, that is why the operator is 2**nqubits x 2**nqubits in size
	##
	## Next, we apply an operator, r, again a 2**nqubits x 2**nqubits matrix, on the state 
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

	## qstretch() and __aligned_op() use two concepts core to
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

	def qstretch(self,op,qbit_list):
		opargs = str(qbit_list)
		if not ugts.qisunitary(oper):
			errmsg = "Error. Operator is not a valid matrix"
			raise QCError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = "User Error. Wrong number of qbit args for operator. Provided arguments = "+opargs+"."
			raise QCError(errmsg)
		c_op = np.kron(op,np.eye(2**(self.nqubits-len(qbit_list))))
		a_op = self.__aligned_op(c_op,qbit_list)
		return a_op

