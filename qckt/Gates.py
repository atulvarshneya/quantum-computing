#!/usr/bin/env python3

import numpy as np
import random as rnd

class GateWrapper:
	def __init__(self, circuit, gateCls):
		self.circuit = circuit
		self.GateCls = gateCls
	def addGate(self, *args, **kwargs):
		gate = self.GateCls(*args, **kwargs)
		self.circuit.append(gate)

class QGate:
	def __init__(self):
		self.qbits = None
		self.cbits = None
		self.gateparams = []
		self.name = None
		self.opMatrix = None

	def _reorderlist(self,oseq,nseq):
		newseq = []
		nqbits = len(nseq)
		for i in oseq:
			newseq.append(nseq[nqbits-i-1])
		return newseq

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		if self.cbits is not None:
			self.cbits = self._reorderlist(self.cbits,newseq)
		return self

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate([self.name,self.opMatrix], self.qbits)

	def __str__(self):
		stringify = self.name
		for p in self.gateparams:
			if type(p) is int:
				pstr = f'{p:d}'
			elif type(p) is float:
				pstr = f'{p:.4f}'
			else:
				pstr = str(p)
			stringify = stringify+"|"+pstr
		stringify = stringify+":"+str(self.qbits)
		if self.cbits is not None:
			stringify = stringify + ":"+str(self.cbits)
		return stringify
		# return self.name+":"+str(self.qbits)

	## Utility function to add control bit
	def CTL(self,opMatrix):
		(r,c) = opMatrix.shape
		oparr = np.array(opMatrix)
		coparr = np.eye(r*2,dtype=complex)
		for i in range(r,r*2):
			for j in range(r,r*2):
				coparr[i][j] = oparr[i-r][j-r]
		return np.matrix(coparr,dtype=complex)

class X(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "X"
		self.opMatrix = np.matrix([[0,1],[1,0]],dtype=complex)
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"X")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class Y(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "Y"
		self.opMatrix = np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"Y")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class Z(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "Z"
		self.opMatrix = np.matrix([[1,0],[0,-1]],dtype=complex)
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"Z")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class H(QGate):
	def __init__(self, qbit):
		super().__init__()
		sqr2 = np.sqrt(2)
		self.qbits = [qbit]
		self.name = "H"
		self.opMatrix = np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"H")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CX(QGate):

	def __init__(self, control, target):
		super().__init__()
		self.qbits = [control, target]
		self.name = "CX"
		self.opMatrix = self.CTL(np.matrix([[0,1],[1,0]],dtype=complex))

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,[".","X"])
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class T(QGate):

	def __init__(self, control1, control2, target):
		super().__init__()
		self.qbits = [control1, control2, target]
		self.name = "T"
		self.opMatrix = self.CTL(self.CTL(np.matrix([[0,1],[1,0]],dtype=complex)))

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,[".",".","X"])
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class SWAP(QGate):

	def __init__(self, qbit1, qbit2):
		super().__init__()
		self.qbits = [qbit1, qbit2]
		self.name = "SWAP"
		self.opMatrix = np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["*","*"])
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class M(QGate):

	def __init__(self, qubitslist, clbitslist=None):
		super().__init__()
		if clbitslist is None:
			clbitslist = qubitslist
		if (type(qubitslist) != list) or (type(clbitslist) != list):
			errmsg = "Error: M gate requires a list of qubits and optionally a list of classical bits as arguments"
			raise qsim.QSimError(errmsg)
		self.qbits = qubitslist
		self.cbits = clbitslist
		self.name = "M"

	def addtocanvas(self,canvas):
		for qb in self.qbits:
			col = canvas._get1col(3)
			st = qb
			en = len(col)//2 - 1
			for i in range(st,en):
				col[2*i] = "-|-"
				col[2*i+1] = " | "
			col[qb*2] = "[M]"
			col[en*2] = "=v="
			canvas._append(col)
			canvas._extend()
		return self

	# INHERIT realign(self,newseq):
	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

	def exec(self,qc):
		# print("exec qc.qmeasure(",str(self),")")
		qc.qmeasure(self.qbits,cbit_list=self.cbits)

class Border(QGate):

	def __init__(self):
		super().__init__()
		self.qbits = []
		self.name = "BORDER"

	def addtocanvas(self,canvas):
		canvas._extend()
		col = canvas._get1col(1)
		en = len(col)//2
		for i in range(en):
			col[2*i] = "#"
			col[2*i+1] = "#"
		canvas._append(col)
		canvas._extend()
		return self

	# INHERIT realign(self,newseq):

	# OVERRIDE exec(self,qc) - nothing to execute
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		pass

	# OVERRIDE __str__(self) - no [qbits]
	def __str__(self):
		return "BORDER"

class QFT(QGate):

	def __init__(self, qbits):
		super().__init__()
		self.qbits = qbits
		self.name = "QFT"

		N = 2**len(self.qbits) # number of rows and cols
		theta = 2.0 * np.pi / N
		opMat = [None]*N
		for i in range(N):
			row = []
			for j in range(N):
				pow = i * j
				pow = pow % N
				# print "w^",pow
				row.append(np.e**(1.j*theta*pow))
			opMat[i] = row
		self.opMatrix = np.matrix(opMat,dtype=complex) / np.sqrt(N)

	def addtocanvas(self,canvas):
		canvas._add_boxed(self.qbits,"QFT")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class RND(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "RND"

		phi = rnd.random() * np.pi * 2
		camp = np.cos(phi)
		samp = np.sin(phi)
		phi = rnd.random() * np.pi * 2
		re1 = camp*np.cos(phi)
		im1 = camp*np.sin(phi)
		re2 = samp*np.cos(phi)
		im2 = samp*np.sin(phi)
		self.OpMatrix = np.matrix([[complex(-re1,-im1),complex(re2,im2)],[complex(re2,im2),complex(re1,im1)]],dtype=complex)
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"RND")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class UROT(QGate):
	def __init__(self, rotphi, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [rotphi]
		self.name = "UROT"

		phi = self.gateparams[0]
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		self.opMatrix = np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"UROT")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CROT(QGate):
	def __init__(self, rotphi, control, target):
		super().__init__()
		self.qbits = [control, target]
		self.gateparams = [rotphi]
		self.name = "CROT"

		phi = self.gateparams[0]
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		self.opMatrix = self.CTL(np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex))

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,[".","UROT"])
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class Rk(QGate):
	def __init__(self, rotk, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [rotk]
		self.name = "Rk"

		k = self.gateparams[0]
		ck = np.cos(2*np.pi/(2**k))
		sk = np.sin(2*np.pi/(2**k))
		self.opMatrix = np.matrix([ [1,0], [0,complex(ck,sk)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"Rk")
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

GatesList = [X,Y,Z,H,CX,T,SWAP,M,Border,QFT,RND,UROT,CROT,Rk]

###################################################
### Support for Custom Gates
###################################################

class CustomGateWrapper:
	def __init__(self, circuit, name, opMatrix):
		self.name = name
		self.opMatrix = opMatrix
		self.circuit = circuit
	def addGate(self, qbits):
		qbitsList = qbits
		if type(qbitsList).__name__ != 'list':
			qbitsList = [qbits]
		gate = CustomGate(self.name, self.opMatrix, qbitsList)
		self.circuit.append(gate)

class CustomGate(QGate):

	def __init__(self, name, opMatrix, qbits):
		super().__init__()
		self.name = name
		self.opMatrix = opMatrix
		self.qbits = qbits

	def addtocanvas(self,canvas):
		canvas._add_boxed(self.qbits,self.name)
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):
	# INHERIT def exec(self,qc):

