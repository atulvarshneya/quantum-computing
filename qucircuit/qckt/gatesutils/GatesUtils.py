#!/usr/bin/python3

import numpy as np
import copy
from qckt.qException import QCktException

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
	qbit_reorder = _qbit_realign_full_list(nqbits, qbit_list)
	(rmat,invrmat) = _rmat_invrmat(nqbits, qbit_reorder)
	a_op = invrmat * oper * rmat
	return a_op


def stretched_opmatrix(nqbits,oper,qbit_list):
	c_op = np.kron(oper,np.eye(2**(nqbits-len(qbit_list))))
	a_op = _aligned_op(nqbits,c_op,qbit_list)
	return a_op

def combine_opmatrices_par(op_list):
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

def combine_opmatrices_seq(op_list):
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

def opmat_dagger(opMat):
	mat = opMat[:]
	invmat = np.conjugate(np.transpose(mat))
	return invmat

## Utility function to add control bit
def CTL(opMatrix):
	(r,c) = opMatrix.shape
	oparr = np.array(opMatrix)
	coparr = np.eye(r*2,dtype=complex)
	for i in range(r,r*2):
		for j in range(r,r*2):
			coparr[i][j] = oparr[i-r][j-r]
	return np.matrix(coparr,dtype=complex)

