
import numpy as np
import qcutilsckt as uckt
from qcerror import *

def qcombine_seq(op_list):
	d = (op_list[0]).shape[0]
	res = np.matrix(np.eye(d),dtype=complex)
	for op in op_list:
		r = op.shape[0]
		c = op.shape[1]
		if r != c:
			errmsg = "Opearion is not a square matrix."
			raise QCError(errmsg)
		if r != d:
			errmsg = "Opearion matrices not the same size."
			raise QCError(errmsg)
		res = op*res # remember order of multiplication is opposite of the visual order
	return res

def qcombine_par(op_list):
	res = None
	first = True
	for mat in op_list:
		if first:
			res = mat
			first = False
		else:
			res = np.kron(res,mat)
	return res

def qinverse(op):
	mat = deepcopy(op)
	invmat = np.conjugate(np.transpose(mat))
	return invmat

def qisunitary(mat):
	(r,c) = mat.shape
	if r != c:
		return False
	invmat = np.conjugate(np.transpose(mat))
	pmat = np.asarray(mat * invmat)
	for i in range(r):
		for j in range(c):
			if i != j:
				if np.absolute(pmat[i][j]) > uckt.maxerr:
					return False
			else:
				if np.absolute(pmat[i][j]-1.0) > uckt.maxerr:
					return False
	return True

