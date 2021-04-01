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
		return self.name+":"+str(self.qbits)

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
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[X]"
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[Y]"
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[Z]"
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[H]"
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(3)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "-|-"
			col[i*2+1] = " | "
		col[self.qbits[0]*2] = "[.]"
		col[self.qbits[1]*2] = "[X]"        
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(3)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "-|-"
			col[i*2+1] = " | "
		col[self.qbits[0]*2] = "[.]"
		col[self.qbits[1]*2] = "[.]"        
		col[self.qbits[2]*2] = "[X]"        
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(3)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "-|-"
			col[i*2+1] = " | "
		col[self.qbits[0]*2] = "[*]"
		col[self.qbits[1]*2] = "[*]"        
		canvas.append(col)
		canvas._extend()
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
			canvas.append(col)
			canvas._extend()
		return self

	# INHERIT realign(self,newseq):
	# INHERIT def realign(self,newseq):

	def exec(self,qc):
		# print("exec qc.qmeasure(",str(self),")")
		qc.qmeasure(self.qbits,cbit_list=self.cbits)

	# OVERRIDE __str__(self) - additionally include cbits
	def __str__(self):
		return "M:"+str(self.qbits)+":"+str(self.cbits)

class Border(QGate):

	def __init__(self):
		super().__init__()
		self.name = "BORDER"

	def addtocanvas(self,canvas):
		canvas._extend()
		col = canvas._get1col(1)
		en = len(col)//2
		for i in range(en):
			col[2*i] = "#"
			col[2*i+1] = "#"
		canvas.append(col)
		canvas._extend()
		return self

	# OVERRIDE realign(self,newseq) - no realignment
	def realign(self,newseq):
		return self

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
		col = canvas._get1col(7)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "|-----|"
			col[i*2+1] = "|     |"
		for q in self.qbits:
			col[q*2] = "[QFT  ]"
		col[self.qbits[0]*2] = "[QFT M]"
		col[self.qbits[-1]*2] = "[QFT L]"
		canvas.append(col)
		canvas._extend()
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
		col = canvas._get1col(5)
		col[self.qbits[0]*2] = "[RND]"
		canvas.append(col)
		canvas._extend()
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class ROT(QGate):
	def __init__(self, phi, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.phi = phi
		self.name = "ROT"

		cphi = np.cos(self.phi)
		sphi = np.sin(self.phi)
		self.opMatrix = np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)

	def addtocanvas(self,canvas):
		col = canvas._get1col(5)
		col[self.qbits[0]*2] = "[ROT]"
		canvas.append(col)
		canvas._extend()
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):

	# OVERRIDE def __str__(self): additional gate config parameter
	def __str__(self):
		return "ROT|"+"{:.4f}".format(self.phi)+":"+str(self.qbits)

class Rk(QGate):
	def __init__(self, k, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.k = k
		self.name = "Rk"

		ck = np.cos(2*np.pi/(2**k))
		sk = np.sin(2*np.pi/(2**k))
		self.opMatrix = np.matrix([ [1,0], [0,complex(ck,sk)]],dtype=complex)

	def addtocanvas(self,canvas):
		col = canvas._get1col(4)
		col[self.qbits[0]*2] = "[Rk]"
		canvas.append(col)
		canvas._extend()
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):

	# OVERRIDE def __str__(self): additional gate config parameter
	def __str__(self):
		return "Rk|"+"{:d}".format(self.k)+":"+str(self.qbits)

GatesList = [X,Y,Z,H,CX,T,SWAP,M,Border,QFT,RND,ROT,Rk]

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
		ncols = len(self.name) + 2 # 2 for '[', ']'
		usegname = self.name
		if (len(self.qbits) > 1):
			ncols += 2 # for ' M' and ' L' to indicate MSB, LSB
			usegname = self.name+"  "
			usegnameM = self.name+" M"
			usegnameL = self.name+" L"
		col = canvas._get1col(ncols)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "|"+ "-"*(ncols-2)+"|"
			col[i*2+1] = "|"+ " "*(ncols-2)+"|"
		for q in self.qbits:
			col[q*2] = "["+usegname+"]"
		if len(self.qbits) > 1:
			col[self.qbits[0]*2] = '['+usegnameM+']'
			col[self.qbits[-1]*2] = '['+usegnameL+']'
		canvas.append(col)
		canvas._extend()
		return self

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):
	# INHERIT def exec(self,qc):

