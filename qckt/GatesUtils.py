#!/usr/bin/python3

import numpy as np
import copy
from qException import QCktException

####################################################################################################
## Utility functions ###############################################################################
####################################################################################################

def _qbit_realign_full_list(nqbits, qbit_list):
	reord_list = copy.deepcopy(qbit_list)
	for i in reversed(range(nqbits)): # reversed to maintain significance order of the other qbits; poetic correctness :-)
		if i not in reord_list:
			reord_list.append(i)
	return reord_list

def _shuffled_count(nqbits, bitorder):
	shuffled = []
	for i in range(2**nqbits):
		shfval = 0
		for b in range(nqbits):
			dstbit = bitorder[nqbits-b-1]  ## (nqbits-1) - b  becasue bitorder is array like [MSB, ...,LSB]
			shfval += (((i >> b) & 0x1) << dstbit)
		shuffled.append(shfval)
	return shuffled

def _rmat_invrmat(nqbits, qbit_reorder): ## why this name? rmat is matrix that reorders the state vector, invrmat is inverse of rmat
	# this is per counting with the given bit ordering
	shfl_svec_idxs = _shuffled_count(nqbits, qbit_reorder)
	## create the rmat and invrmat
	imat = np.matrix(np.eye(2**nqbits))
	rmat = np.matrix(np.eye(2**nqbits))
	invrmat = np.matrix(np.eye(2**nqbits))
	for i in range(2**nqbits):
		s = shfl_svec_idxs[i]
		rmat[i] = imat[s]
		invrmat[s] = imat[i]
	return (rmat, invrmat)

def _aligned_op(nqbits, oper, qbit_list):
	"""
	qbit_reorder is 'visually correct'. So [a,b,c,d] implies bring to MSB 
	the bit in position 'a' in the original, brint to the next lower MSB 
	the bit in potion 'b' in the original, and so on ...
	"""
	qbit_reorder = _qbit_realign_full_list(nqbits, qbit_list)
	(rmat,invrmat) = _rmat_invrmat(nqbits, qbit_reorder)
	a_op = invrmat * oper * rmat
	return a_op

	## stretched_opmatrix() and aligned_op() use two concepts core to
	## the working of this simulator.

def stretched_opmatrix(nqbits,oper,qbit_list):
	if (2**len(qbit_list)) != (oper.shape)[0]:
		opargs = str(qbit_list)
		errmsg = "User Error. Wrong number of qbit args for operator "
		raise QCktException(errmsg)
	c_op = np.kron(oper,np.eye(2**(nqbits-len(qbit_list))))
	a_op = _aligned_op(nqbits,c_op,qbit_list)
	return a_op

def qcombine_par(op_list):
	res = None
	first = True
	for op in op_list:
		mat = op
		if first:
			res = op
			first = False
		else:
			res = np.kron(res,op)
	return res

def qcombine_seq(op_list):
	d = (op_list[0]).shape[0]
	res = np.matrix(np.eye(d),dtype=complex)
	for op in op_list:
		r = op.shape[0]
		c = op.shape[1]
		if r != c:
			errmsg = "Operation is not a square matrix."
			raise QCktException(errmsg)
		if r != d:
			errmsg = "Operation matrices not the same size."
			raise QCktException(errmsg)
		res = op*res # remember order of multiplication is opposite of the visual order
	return res

def isunitary(mat):
	floaterr = 10**(-8)
	if type(mat) is not np.matrix:
		return False
	(r,c) = mat.shape
	if r != c:
		return False
	invmat = np.conjugate(np.transpose(mat))
	pmat = np.asarray(mat * invmat)
	for i in range(r):
		for j in range(c):
			if i != j:
				if np.absolute(pmat[i][j]) > floaterr:
					return False
			else:
				if np.absolute(pmat[i][j]-1.0) > floaterr:
					return False
	return True

if __name__ == "__main__":
	print("valid_qbit_list() tests ---------------------------------")
	res = valid_qbit_list(4,[2,3,3,0])
	print(res)
	res = valid_qbit_list(4,[2,1,3,0,5])
	print(res)
	res = valid_qbit_list(4,[2,1,3,5])
	print(res)
	res = valid_qbit_list(4,[2,1,3,0])
	print(res)

	print("stretched_opmatrix() tests ---------------------------------")
	def print_state(nqbits,state):
		maxerror = 10**(-8)
		for i in range(len(state)):
			if state[i] > maxerror:
				print(("{0:0"+str(nqbits)+"b}    ").format(i),state[i].item(0))
	nqbits = 4
	qbit_listx = [1,0]
	operx = np.matrix([[0,1],[1,0]],dtype=complex)
	operxx = np.kron(operx,operx)
	qbit_list1 = [1,0]
	oper1 = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)
	qbit_list2 = [3,2]
	oper2 = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)
	state = [None]*(2**nqbits)
	for i in range(2**nqbits):
		if i == 3 or i == 12:
			state[i] = 1.0
		else:
			state[i] = 0.0
	state = np.transpose(np.matrix(state,dtype=complex))
	aop1 = stretched_opmatrix(nqbits,oper1,qbit_list1)
	aop2 = stretched_opmatrix(nqbits,oper2,qbit_list2)
	aopx = stretched_opmatrix(nqbits,operxx,qbit_listx)
	if qisunitary(aop1):
		print("aop1 is unitary")
	else:
		print("aop1 is NOT unitary")
	if qisunitary(aop2):
		print("aop2 is unitary")
	else:
		print("aop2 is NOT unitary")
	if qisunitary(aopx):
		print("aopx is unitary")
	else:
		print("aopx is NOT unitary")
	print("Original state")
	print_state(nqbits,state)
	print("state after aop1")
	print_state(nqbits,aop1 * state)
	print("state after aop2")
	print_state(nqbits,aop2 * state)
	print("state after aopx")
	print_state(nqbits,aopx * state)
	print("combined_seq/par() tests ---------------------------------")
	aopS = qcombine_seq([aop1,aop2,aopx])
	print("state after aopS")
	print_state(nqbits,aopS * state)
	aopP = qcombine_par([oper1,oper2])
	print("state after aopP")
	print_state(nqbits,aopP * state)
