
import numpy as np
from qsim.qSimException import *
import random as rnd
import qsim.qgatesUtils as qgu

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
	Phase rotation gate. Takes the k as an argument to divide 2*pi by 2**k.
	"""
	ck = np.cos(2*np.pi/(2**k))
	sk = np.sin(2*np.pi/(2**k))
	return ["ROTk({:d})".format(k), np.matrix([
		[1,0],
		[0,complex(ck,sk)]],dtype=complex)]

def SQSWAP():
	"""
	Square-root of Swap gate.
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
	return qgu.qcombine_par("H**{:d}".format(n),op_list)

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

