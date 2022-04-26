
import numpy as np
from qSimException import *
import random as rnd

## QC Gates
def X():
	"""
	Pauli_X gate.
	"""
	return ["X", np.matrix([[0,1],[1,0]],dtype=complex)]

def Y():
	"""
	Pauli_Y gate.
	"""
	return ["Y", np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]

def Z():
	"""
	Pauli_Z gate.
	"""
	return ["Z", np.matrix([[1,0],[0,-1]],dtype=complex)]

def H():
	"""
	Hadamard gate.
	"""
	sqr2 = np.sqrt(2)
	return ["HADAMARD", np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)]

def Rphi(phi):
	"""
	Phase rotation gate. Takes the Phi as an argument.
	"""
	cphi = np.cos(phi)
	sphi = np.sin(phi)
	return ["ROTphi({:0.4f})".format(phi), np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)]

def Rk(k):
	"""
	Controlled Phase rotation gate. Takes the k as an argument to divide 2*pi by 2**k.
	"""
	ck = np.cos(2*np.pi/(2**k))
	sk = np.sin(2*np.pi/(2**k))
	return ["ROTk({:d})".format(k), np.matrix([
		[1,0],
		[0,complex(ck,sk)]],dtype=complex)]

def SQSWAP():
	"""
	Swap gate.
	"""
	return ["SQSWAP", np.matrix([[1,0,0,0],[0,0.5+0.5j,0.5-0.5j,0],[0,0.5-0.5j,0.5+0.5j,0],[0,0,0,1]],dtype=complex)]

def SWAP():
	"""
	Swap gate.
	"""
	return ["SWAP", np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)]

def CSWAP():
	"""
	CSWAP gate
	"""
	return CTL(SWAP())

def QFT(nqbits):
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

def Hn(n):
	"""
	H^n gate - very commonly used
	"""
	op_list = []
	for i in range(n):
		op_list.append(H())
	return qcombine_par("H**{:d}".format(n),op_list)

def RND():
	"""
	Random apmplitude gate.
	"""
	phi = rnd.random() * np.pi * 2
	camp = np.cos(phi)
	samp = np.sin(phi)
	phi = rnd.random() * np.pi * 2
	re1 = camp*np.cos(phi)
	im1 = camp*np.sin(phi)
	re2 = samp*np.cos(phi)
	im2 = samp*np.sin(phi)
	return ["RND", np.matrix([[complex(-re1,-im1),complex(re2,im2)],[complex(re2,im2),complex(re1,im1)]],dtype=complex)]

def CTL(op,name=None):
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

def C():
	"""
	CNOT gate
	"""
	return CTL(X(),name="CNOT")

def T():
	"""
	TOFFOLI gate.
	"""
	return CTL(CTL(X()),name="TOFFOLI")

# Basis Matrices
def BELL_BASIS():
	return ["BELL_BASIS",np.matrix([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]], dtype=complex)/np.sqrt(2)]

def HDM_BASIS():
	sq2 = np.sqrt(2)
	return ["HDM_BASIS",np.matrix([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)]

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
			raise QSimError(errmsg)
		if r != d:
			errmsg = "Operation matrices not the same size."
			raise QSimError(errmsg)
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
