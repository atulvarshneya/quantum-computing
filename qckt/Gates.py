#!/usr/bin/env python3

import numpy as np
import random as rnd
import GatesUtils as gutils
from qException import QCktException

class GateWrapper:
	def __init__(self, qckt, gateCls):
		self.qckt = qckt
		self.GateCls = gateCls
	def addGate(self, *args, **kwargs):
		gate = self.GateCls(*args, **kwargs)
		gate.addtoqckt(self.qckt)
		return self.qckt

class QGate:
	def __init__(self):
		self.qckt = None
		self.qbits = None
		self.cbits = None
		self.gateparams = []
		self.name = None
		self.opMatrix = None

	def _reorderlist(self,oseq,nseq):
		newseq = []
		nqbits = len(nseq)
		for i in oseq:
			if issubclass(type(i),list):
				newseq.append(self._reorderlist(i,nseq))
			else:
				newseq.append(nseq[nqbits-i-1])
		return newseq

	def addtoqckt(self, qckt):
		self.qckt = qckt
		qckt.circuit.append(self)
		if self.check_qbit_args() == False:
			errmsg = "Error: qubit arguments incorrect. " + self.name + str(self.qbits)
			raise QCktException(errmsg)

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		if self.cbits is not None:
			self.cbits = self._reorderlist(self.cbits,newseq)
		return self

	def exec(self,qsim):
		# print("exec qsim.qgate(",str(self),")")
		if issubclass(type(self.qbits[0]),list) and len(self.qbits) == 1:
			for q in self.qbits[0]:
				qsim.qgate([self.name,self.opMatrix], [q])
		else:
			qsim.qgate([self.name,self.opMatrix], self.qbits)

	def to_fullmatrix(self):
		(nqbits,_) = self.qckt.get_size()
		oplist = []
		if issubclass(type(self.qbits[0]),list) and len(self.qbits) == 1:
			for q in self.qbits[0]:
				op = gutils.stretched_opmatrix(nqbits,self.opMatrix,[q])
				oplist.append(op)
			opmat = gutils.combine_seq(oplist)
		else:
			opmat = gutils.stretched_opmatrix(nqbits,self.opMatrix,self.qbits)
		return opmat

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

	##############################################################################
	## Args validation methods
	##############################################################################

	def check_qbit_args(self):
		## to be overridden by individual gates
		print("TODO: Arcgs validation missing for ",type(self).__name__)

	def oneqbit_args(self,qbits_list=None):
		multiqbits = []
		retval = None
		qbits = self.qbits
		if qbits_list is not None:
			qbits = qbits_list
		if len(qbits) == 1:
			if type(qbits[0]) is int:
				multiqbits = self.qbits
				retval = None # just asserting that retval is None here
			elif issubclass(type(qbits[0]),list):
				if len(qbits[0]) > 0:
					retval = None # just asserting that retval is None here
					for q in qbits[0]:
						if type(q) is int:
							multiqbits.append(q)
						else:
							retval = False
				else:
					retval = False
			else:
				retval = False
		else:
			retval = False
		if retval is None:
			retval = self.isvalid_qbits_gen(multiqbits)
		return retval

	def fixedqbit_args(self,nq,qbits_list=None):
		multiqbits = []
		retval = None
		qbits = self.qbits
		if qbits_list is not None:
			qbits = qbits_list
		if len(qbits) == nq:
			for q in qbits:
				if type(q) is int:
					multiqbits.append(q)
				else:
					retval = False
		else:
			retval = False
		if retval is None:
			retval = self.isvalid_qbits_gen(multiqbits)
		return retval

	def varqbit_args(self, minnq, qbits_list=None):
		multiqbits = []
		retval = None
		qbits = self.qbits
		if qbits_list is not None:
			qbits = qbits_list
		if len(qbits) >= minnq:
			for q in qbits:
				if type(q) is int:
					multiqbits.append(q)
				else:
					retval = False
		else:
			retval = False
		if retval is None:
			retval = self.isvalid_qbits_gen(multiqbits)
		return retval

	def isvalid_qbits_gen(self,qbit_list):
		nqbits,_ = self.qckt.get_size()
		if len(qbit_list) > nqbits:
			return False
		for i in qbit_list:
			if i >= nqbits:
				return False
			if qbit_list.count(i) != 1:
				return False
		return True

class X(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "X"
		self.opMatrix = np.matrix([[0,1],[1,0]],dtype=complex)
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"X")
		return self

	def check_qbit_args(self):
		return self.oneqbit_args()

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

	def check_qbit_args(self):
		return self.oneqbit_args()

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

	def check_qbit_args(self):
		return self.oneqbit_args()

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

	def check_qbit_args(self):
		return self.oneqbit_args()

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CX(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.name = "CX"
		self.opMatrix = np.matrix([[0,1],[1,0]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = self.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["X"])
		return self

	def check_qbit_args(self):
		return self.varqbit_args(2)

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CY(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.name = "CY"
		self.opMatrix = np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = self.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Y"])
		return self

	def check_qbit_args(self):
		return self.varqbit_args(2)

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CZ(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.name = "CZ"
		self.opMatrix = np.matrix([[1,0],[0,-1]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = self.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Z"])
		return self

	def check_qbit_args(self):
		return self.varqbit_args(2)

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):


class CCX(QGate):

	def __init__(self, control1, control2, target):
		super().__init__()
		self.qbits = [control1, control2, target]
		self.name = "CCX"
		self.opMatrix = self.CTL(self.CTL(np.matrix([[0,1],[1,0]],dtype=complex)))

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,[".",".","X"])
		return self

	def check_qbit_args(self):
		return self.fixedqbit_args(3)

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

	def check_qbit_args(self):
		return self.fixedqbit_args(2)

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class M(QGate):

	def __init__(self, qubitslist, clbitslist=None):
		super().__init__()
		if clbitslist is None:
			clbitslist = qubitslist
		if (not issubclass(type(qubitslist),list)) or (not issubclass(type(clbitslist),list)):
			errmsg = "Error: M gate requires a list of qubits and optionally a list of classical bits as arguments"
			raise QCktException(errmsg)
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

	def check_qbit_args(self):
		retval = True
		if len(self.qbits) != len(self.cbits):
			retval = False
		if not self.varqbit_args(1):
			retval = False
		if not self.varqbit_args(1,qbits_list=self.cbits):
			retval = False
		return retval

	# INHERIT realign(self,newseq):
	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

	def to_fullmatrix(self):
		errmsg = "Measure gate cannot be converted to opmatrix."
		raise QCktException(errmsg)

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

	def check_qbit_args(self):
		pass

	# INHERIT realign(self,newseq):

	def to_fullmatrix(self):
		return None

	# OVERRIDE exec(self,qc) - nothing to execute
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		pass

	# OVERRIDE __str__(self) - no [qbits]
	def __str__(self):
		return "BORDER"

class Probe(QGate):

	def __init__(self, header="",probestates=None,probeobject=None):
		super().__init__()
		self.qbits = []
		self.header = "PROBE: "+header
		self.probestates = probestates
		self.probeobject = probeobject
		self.name = "Probe"

	def addtocanvas(self,canvas):
		canvas._extend()
		col = canvas._get1col(1)
		en = len(col)//2
		for i in range(en):
			col[2*i] = "v"
			col[2*i+1] = "V"
		canvas._append(col)
		canvas._extend()
		return self

	def check_qbit_args(self):
		pass

	# INHERIT realign(self,newseq):

	def to_fullmatrix(self):
		return None

	# OVERRIDE exec(self,qc) - nothing to execute
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		nqbits = qc.qsize()
		(creglist, sveclist) = qc.qsnapshot()
		if self.probeobject is not None:
			self.probeobject.analyze(creglist,sveclist)
		print(self.header)
		for i in range(len(sveclist)):
			if (self.probestates is None and abs(sveclist[i]) > 0.0) \
					or (self.probestates is not None and i in self.probestates):
				print(("{0:0"+str(nqbits)+"b}    {1:.8f}").format(i, sveclist[i]))
		cregsz = len(creglist)
		print("CREGISTER: ",end="")
		for i in range(cregsz):
			print("{:01b}".format(creglist[i]),end="")
		print()

	# OVERRIDE __str__(self) - no [qbits]
	def __str__(self):
		return "PROBE"

class ProbeAnalyzer:
	'if an object of ProbeAnalyzer class is passed in Probe gate, its analyze() method is called when Probe gate is invoked.'
	def __init__(self):
		pass
	def analyze(self,creglist,sveclist):
		pass


class QFT(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		if len(allqbits) == 1 and issubclass(type(allqbits[0]),list):
			self.qbits = allqbits[0]
		else:
			self.qbits = list(allqbits)
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

	def check_qbit_args(self):
		return self.varqbit_args(1)

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

	def check_qbit_args(self):
		return self.oneqbit_args()

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class P(QGate):
	def __init__(self, rotphi, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [rotphi]
		self.name = "P"

		phi = self.gateparams[0]
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		self.opMatrix = np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"P")
		return self

	def check_qbit_args(self):
		return self.oneqbit_args()

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CP(QGate):

	def __init__(self, rotphi, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [rotphi]
		self.name = "CP"

		phi = self.gateparams[0]
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		self.opMatrix = np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = self.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["P"])
		return self

	def check_qbit_args(self):
		return self.varqbit_args(2)

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class UROTk(QGate):
	def __init__(self, rotk, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [rotk]
		self.name = "UROTk"

		k = self.gateparams[0]
		ck = np.cos(2*np.pi/(2**k))
		sk = np.sin(2*np.pi/(2**k))
		self.opMatrix = np.matrix([ [1,0], [0,complex(ck,sk)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"UROTk")
		return self

	def check_qbit_args(self):
		return self.oneqbit_args()

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CROTk(QGate):
	def __init__(self, rotk, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [rotk]
		self.name = "CROTk"

		k = self.gateparams[0]
		ck = np.cos(2*np.pi/(2**k))
		sk = np.sin(2*np.pi/(2**k))
		self.opMatrix = np.matrix([ [1,0], [0,complex(ck,sk)]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = self.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"])
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["UROTk"])
		return self

	def check_qbit_args(self):
		return self.varqbit_args(2)

	# INHERIT def realign(self,newseq):
	# INHERIT def exec(self,qc):
	# INHERIT def __str__(self):

class CUSTOM(QGate):

	def __init__(self, name, opMatrix, qbits):
		super().__init__()
		self.name = name
		if not gutils.isunitary(opMatrix):
			errmsg = "Custom gate, "+self.name+", operator matrix is not unitary."
			raise QCktException(errmsg)
		self.opMatrix = opMatrix
		self.qbits = qbits

	def addtocanvas(self,canvas):
		canvas._add_boxed(self.qbits,self.name)
		return self

	def check_qbit_args(self):
		r,c = self.opMatrix.shape
		if 2**len(self.qbits) != r:
			return False
		return self.varqbit_args(1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):
	# INHERIT def exec(self,qc):


GatesList = [X,Y,Z,H,CX,CY,CZ,CCX,SWAP,M,Border,Probe,QFT,RND,P,CP,UROTk,CROTk,CUSTOM]
