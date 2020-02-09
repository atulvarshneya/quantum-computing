#!/usr/bin/python3

# This file is part of the QCLIB project covered under GPL v3 license.
# See the full license in the file LICENSE
# Author: Atul Varshneya

import numpy as np
import random as rnd
import qcutilsgts as ugts
from qcerror import *

class qcgates:

	def __init__(self):
		self.gate_dict = {
			"X": self.X(),
			"Y": self.Y(),
			"Z": self.Z(),
			"C": self.C(),
			"H": self.H(),
			"T": self.T(),
			"SQSWAP": self.SQSWAP(),
			"SWAP": self.SWAP(),
			"CSWAP": self.CSWAP(),
			"RND": self.RND(),
			"M": ["M"]
			}

	def listops(self):
		return self.gate_dict.keys()

	def getop(self, qcgate):
		return self.gate_dict[qcgate]

	def validate_gate(self, qcgate):
		if not (qcgate in self.gate_dict.keys()):
			return False
		else:
			return True

	def validate_gate_args(self, qcgate, qubits):
		## check number of qubits required for this gate
		if qcgate == "M":
			return True
		op = (self.gate_dict[qcgate])
		if (2**len(qubits)) != (op.shape)[0]:
			return False
		else:
			return True

	def mkgate(self,gtname, gtmatrix):
		if gtname in self.gate_dict.keys():
			raise QCError("mkgate error. gate name already exists: {}".format(gtname))
		if not ugts.qisunitary(gtmatrix):
			raise QCError("mkgate error - gate matrix is not unitary: {}".format(gtnam))
		self.gate_dict[gtname] = gtmatrix
		return gtmatrix

	## QC Gates
	def X(self):
		"""
		Pauli_X gate.
		"""
		return np.matrix([[0,1],[1,0]],dtype=complex)

	def Y(self):
		"""
		Pauli_Y gate.
		"""
		return np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)

	def Z(self):
		"""
		Pauli_Z gate.
		"""
		return np.matrix([[1,0],[0,-1]],dtype=complex)

	def C(self):
		"""
		CNOT gate
		"""
		return self.ADD_CTL(self.X())

	def H(self):
		"""
		Hadamard gate.
		"""
		sqr2 = np.sqrt(2)
		return np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)

	def T(self):
		"""
		TOFFOLI gate.
		"""
		return self.ADD_CTL(self.ADD_CTL(self.X()))

	def SQSWAP(self):
		"""
		Swap gate.
		"""
		return np.matrix([[1,0,0,0],[0,0.5+0.5j,0.5-0.5j,0],[0,0.5-0.5j,0.5+0.5j,0],[0,0,0,1]],dtype=complex)

	def SWAP(self):
		"""
		Swap gate.
		"""
		return np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)

	def CSWAP(self):
		"""
		CSWAP gate
		"""
		return self.ADD_CTL(self.SWAP())

	def RND(self):
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
		return np.matrix([[complex(-re1,-im1),complex(re2,im2)],[complex(re2,im2),complex(re1,im1)]],dtype=complex)

	def ADD_CTL(self,opmat):
		"""
		Add Control to any gate
		"""
		(r,c) = opmat.shape
		oparr = np.array(opmat)
		coparr = np.eye(r*2,dtype=complex)
		for i in range(r,r*2):
			for j in range(r,r*2):
				coparr[i][j] = oparr[i-r][j-r]
		return np.matrix(coparr,dtype=complex)

'''

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

'''

if __name__ == "__main__":
	gt = qcgates()
	v = gt.validate_gate("C",[1,2,3])
	print("gate validation = ", v)
	v = gt.validate_gate("C",[1,2])
	print("gate validation = ", v)
