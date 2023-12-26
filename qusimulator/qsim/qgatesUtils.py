
import numpy as np
import qsim

## qcombine_seq(name,op_list):
##
## Just multiply the operation matrices
def qcombine_seq(name,op_list):
	d = ((op_list[0])[1]).shape[0]
	res = np.matrix(np.eye(d),dtype=complex)
	for opdef in op_list:
		op = opdef[1]
		r = op.shape[0]
		c = op.shape[1]
		if r != c:
			errmsg = "Operation is not a square matrix."
			raise qsim.QSimError(errmsg)
		if r != d:
			errmsg = "Operation matrices not the same size."
			raise qsim.QSimError(errmsg)
		res = op*res # remember order of multiplication is opposite of the visual order
	return [name,res]


## qcombine_par(name,op_list):
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

def qcombine_par(name,op_list):
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
