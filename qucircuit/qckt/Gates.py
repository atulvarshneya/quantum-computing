#!/usr/bin/env python3

import sys
import numpy as np
import random as rnd
import qckt.gatesutils as gutils
import qckt.noisemodel as ns
from qckt.qException import QCktException

class QGate:
	def __init__(self):
		self.qbits = None
		self.cbits = None
		self.gateparams = []
		self.name = None
		self.opMatrix = None
		self.cbit_cond = None
		self.noise_chan = None

	def _reorderlist(self,oseq,nseq):
		newseq = []
		nqbits = len(nseq)
		for i in oseq:
			if issubclass(type(i),list):
				newseq.append(self._reorderlist(i,nseq))
			else:
				newseq.append(nseq[nqbits-i-1])
		return newseq

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		if self.cbits is not None:
			self.cbits = self._reorderlist(self.cbits,newseq)
		return self

	def __check_and_update_opmatrix_for_qubitlist__(self):
		ret_opMatrix = self.opMatrix
		ret_qbits = self.qbits
		if issubclass(type(self.qbits[0]),list):
			# combine_par to create opMatrix to convert from 1-qubit to multiple qubits
			opMatList = [self.opMatrix for _ in range(len(self.qbits[0]))]
			ret_opMatrix = gutils.combine_opmatrices_par(op_list=opMatList)
			ret_qbits = self.qbits[0]
			# print(f'gate {self.name} shape {opMatrix.shape} qubits are a list = {qbits}', file=sys.stderr)
		return ret_opMatrix, ret_qbits

	def assemble(self, noise_profile, noise_profile_gates):
		noise_chan = self.get_gate_noise(noise_profile_gates)
		noise_opseq = ns.consolidate_gate_noise(noise_profile=noise_profile, gate_noise=noise_chan, qubit_list=self.qbits)
		return {"op":"gate","name":self.name,"opMatrix":self.opMatrix,"qubits":self.qbits, 'ifcbit': self.cbit_cond, 'noiseChan':noise_opseq}

	def to_fullmatrix(self,nqbits):
		oplist = []
		if issubclass(type(self.qbits[0]),list) and len(self.qbits) == 1:
			for q in self.qbits[0]:
				op = gutils.stretched_opmatrix(nqbits,self.opMatrix,[q])
				oplist.append(op)
			opmat = gutils.combine_opmatrices_seq(oplist)
		else:
			opmat = gutils.stretched_opmatrix(nqbits,self.opMatrix,self.qbits)
		return opmat

	def ifcbit(self,cbit,val):
		self.cbit_cond = (cbit,val)
		return self
	
	def set_noise(self, noise_chan):  # noise_chan can be NoiseChannel or NoiseChannelSequence
		# don't need to check NoiseChannel or NoiseChannelSequence, consolidate_gate_noise() checks that and converts
		if self.check_noise_op_multi_qubits(noise_chan) == False:
			raise QCktException(f"Error: set_noise() - multi-qubit noise operator, {noise_chan.name},  can't be used on gate {self.name}")
		self.noise_chan = noise_chan
		return self
	
	def check_noise_op_multi_qubits(self, noise_chan):
		if noise_chan is not None:
			if type(noise_chan) is not ns.NoiseChannel and type(noise_chan) is not ns.NoiseChannelSequence:
				raise QCktException(f"ERROR: NoiseChannel or NoiseChannelSequence object or None expected.")
			if type(noise_chan) is ns.NoiseChannel:
				if noise_chan.nqubits != 1 and len(self.qbits) != noise_chan.nqubits:
					return False
			else:  # type is ns.NoiseChannelSequence
				for op in noise_chan:
					if op.nqubits != 1 and len(self.qbits) != op.nqubits:
						return False
		return True

	def addtocanvas_gatenoise(self, canvas, noise_profile, noise_profile_gates):
		noise_chan = self.get_gate_noise(noise_profile_gates)
		noise_opseq = ns.consolidate_gate_noise(noise_profile=noise_profile, gate_noise=noise_chan, qubit_list=self.qbits)
		for kop,qbt in noise_opseq:
			canvas._add_simple(qbt,f'{self.name}:{kop.name}')

	def get_gate_noise(self, noise_profile_gates):
		# pick from noise on gate type, and noise on gate instance
		noise_chan = noise_profile_gates.get(self.__class__, None)
		if self.check_noise_op_multi_qubits(noise_chan) == False:
			raise QCktException(f"Error: add_noise_to_all() - multi-qubit noise operator, {noise_chan.name},  can't be used on gate {self.name}")
		if self.noise_chan is not None:
			noise_chan = self.noise_chan
		return noise_chan
	
	def is_noise_step(self):  # is a step after which 'allsteps' noise should be applied
		return True

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

	##############################################################################
	## Args validation methods
	##############################################################################

	def check_qbit_args(self,nqbits):
		## to be overridden by individual gates
		print("TODO: Args validation missing for ",type(self).__name__)

	def oneqbit_args(self,nqbits,qbits_list=None):
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
			retval = self.isvalid_qbits_gen(nqbits,multiqbits)
		return retval

	def fixedqbit_args(self,nqbits,nfixedq,qbits_list=None):
		multiqbits = []
		retval = None
		qbits = self.qbits
		if qbits_list is not None:
			qbits = qbits_list
		if len(qbits) == nfixedq:
			for q in qbits:
				if type(q) is int:
					multiqbits.append(q)
				else:
					retval = False
		else:
			retval = False
		if retval is None:
			retval = self.isvalid_qbits_gen(nqbits,multiqbits)
		return retval

	def varqbit_args(self, nqbits, minnq, qbits_list=None):
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
			retval = self.isvalid_qbits_gen(nqbits, multiqbits)
		return retval

	def isvalid_qbits_gen(self,nqbits,qbit_list):
		if len(qbit_list) > nqbits:
			return False
		for i in qbit_list:
			if i >= nqbits:
				return False
			if qbit_list.count(i) != 1:
				return False
		return True

# Decorator to regiter the gate class in the GatesList list
GatesList = []
def registerGate(gateclass):
	GatesList.append(gateclass)
	return gateclass

@registerGate
class NOISE(QGate):
	def __init__(self, noise_chan, qbit):
		super().__init__()
		self.qbits = qbit
		if type(noise_chan) is ns.NoiseChannel:
			noise_chan = ns.NoiseChannelSequence(noise_chan)
		self.noise_chan = noise_chan
		self.name = self.noise_chan.name

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits, f'NS:{self.name}')

	def addtocanvas_gatenoise(self, canvas, noise_profile, noise_profile_gates):
		pass

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	def assemble(self, noise_profile, noise_profile_gates):
		noise_chan = self.noise_chan
		if type(noise_chan) is ns.NoiseChannel:
			print('Internal warning: found NOISE noise_chan of class NoiseOperator', file=sys.stderr)
			noise_chan = ns.NoiseChannelSequence(self.noise_chan)
		return {"op":"noise","name":self.name,"noiseChan":noise_chan,"qubits":self.qbits}

	def to_fullmatrix(self,nqbits):
		return None

	def is_noise_step(self):
		return False

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class X(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "X"
		self.opMatrix = np.matrix([[0,1],[1,0]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"X", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class Y(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "Y"
		self.opMatrix = np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"Y", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class Z(QGate):
	def __init__(self, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.name = "Z"
		self.opMatrix = np.matrix([[1,0],[0,-1]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"Z", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class H(QGate):
	def __init__(self, qbit):
		super().__init__()
		sqr2 = np.sqrt(2)
		self.qbits = [qbit]
		self.name = "H"
		self.opMatrix = np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()
	
	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"H", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class CX(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.name = "CX"
		self.opMatrix = np.matrix([[0,1],[1,0]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["X"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class CY(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.name = "CY"
		self.opMatrix = np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Y"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class CZ(QGate):

	def __init__(self, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.name = "CZ"
		self.opMatrix = np.matrix([[1,0],[0,-1]],dtype=complex)
		for i in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Z"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):


@registerGate
class CCX(QGate):

	def __init__(self, control1, control2, target):
		super().__init__()
		self.qbits = [control1, control2, target]
		self.name = "CCX"
		self.opMatrix = gutils.CTL(gutils.CTL(np.matrix([[0,1],[1,0]],dtype=complex)))

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,[".",".","X"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.fixedqbit_args(nqbits,3)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class SWAP(QGate):

	def __init__(self, qbit1, qbit2):
		super().__init__()
		self.qbits = [qbit1, qbit2]
		self.name = "SWAP"
		self.opMatrix = np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["*","*"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.fixedqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
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

	def addtocanvas_gatenoise(self, canvas, noise_profile, noise_profile_gates):
		pass

	def check_qbit_args(self,nqbits):
		retval = True
		if len(self.qbits) != len(self.cbits):
			retval = False
		if not self.varqbit_args(nqbits,1):
			retval = False
		if not self.varqbit_args(nqbits,1,qbits_list=self.cbits):
			retval = False
		return retval

	def ifcbit(self,cbit,val):
		raise QCktException("M gate does not support ifcbit()")

	# INHERIT realign(self,newseq):
	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

	def to_fullmatrix(self,nqbits):
		errmsg = "Measure gate cannot be converted to opmatrix."
		raise QCktException(errmsg)

	def assemble(self, noise_profile, noise_profile_gates):
		return {"op":"measure", "qubits":self.qbits, "clbits":self.cbits}

	def is_noise_step(self):
		return False

@registerGate
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

	def addtocanvas_gatenoise(self, canvas, noise_profile, noise_profile_gates):
		pass

	def check_qbit_args(self,nqbits):
		pass

	def ifcbit(self,cbit,val):
		raise QCktException("Border does not support ifcbit()")

	# INHERIT realign(self,newseq):

	def to_fullmatrix(self,nqbits):
		return None

	def assemble(self, noise_profile, noise_profile_gates):
		return {"op":"noop"}

	def is_noise_step(self):
		return False

	# OVERRIDE __str__(self) - no [qbits]
	def __str__(self):
		return "BORDER"

@registerGate
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
			col[2*i+1] = "v"
		canvas._append(col)
		canvas._extend()
		return self

	def addtocanvas_gatenoise(self, canvas, noise_profile, noise_profile_gates):
		pass

	def check_qbit_args(self,nqbits):
		pass

	def ifcbit(self,cbit,val):
		raise QCktException("Probe does not support ifcbit()")

	# INHERIT realign(self,newseq):

	def to_fullmatrix(self,nqbits):
		return None

	def assemble(self, noise_profile, noise_profile_gates):
		return {"op":"probe","header":self.header,"probestates":self.probestates}

	def is_noise_step(self):
		return False

	# OVERRIDE __str__(self) - no [qbits]
	def __str__(self):
		return "PROBE"

class ProbeAnalyzer:
	'if an object of ProbeAnalyzer class is passed in Probe gate, its analyze() method is called when Probe gate is invoked.'
	def __init__(self):
		pass
	def analyze(self,creglist,sveclist):
		pass


@registerGate
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
		canvas._add_boxed(self.qbits,"QFT", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
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
		self.opMatrix = np.matrix([[complex(-re1,-im1),complex(re2,im2)],[complex(re2,im2),complex(re1,im1)]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"RND", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
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
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"P", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
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
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["P"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
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
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"UROTk", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
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
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"], self.cbit_cond)
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["UROTk"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class Rx(QGate):
	def __init__(self, theta, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [theta]
		self.name = "Rx"

		rot = self.gateparams[0]
		ck = np.cos(rot/2)
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(0,-sk)], [complex(0,-sk),complex(ck,0)]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"Rx", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class CRx(QGate):
	def __init__(self, theta, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [theta]
		self.name = "CRx"

		rot = self.gateparams[0]
		ck = np.cos(rot/2)
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(0,-sk)], [complex(0,-sk),complex(ck,0)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"], self.cbit_cond)
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Rx"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):


@registerGate
class Ry(QGate):
	def __init__(self, theta, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [theta]
		self.name = "Ry"

		rot = self.gateparams[0]
		ck = np.cos(rot/2)
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(-sk,0)], [complex(sk,0),complex(ck,0)]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"Ry", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class CRy(QGate):
	def __init__(self, theta, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [theta]
		self.name = "CRy"

		rot = self.gateparams[0]
		ck = np.cos(rot/2)
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(-sk,0)], [complex(sk,0),complex(ck,0)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"], self.cbit_cond)
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Ry"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):


@registerGate
class Rz(QGate):
	def __init__(self, theta, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [theta]
		self.name = "Rz"

		rot = self.gateparams[0]
		ck = np.cos(rot/2)
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,-sk),complex(0,0)], [complex(0,0),complex(ck,sk)]],dtype=complex)
		self.opMatrix, self.qbits = self.__check_and_update_opmatrix_for_qubitlist__()

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits,"Rz", self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,1)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

@registerGate
class CRz(QGate):
	def __init__(self, theta, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [theta]
		self.name = "CRz"

		rot = self.gateparams[0]
		ck = np.cos(rot/2)
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,-sk),complex(0,0)], [complex(0,0),complex(ck,sk)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"], self.cbit_cond)
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Rz"], self.cbit_cond)
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):


def fetch_custom_gateclass(cgate_name, opMatrix):
	class CUSTOM(QGate):
		def __init__(self, *qbits):
			super().__init__()
			self.name = cgate_name
			if not gutils.isunitary(opMatrix):
				errmsg = f"Custom gate, {self.name}, operator matrix is not unitary."
				raise QCktException(errmsg)
			self.opMatrix = opMatrix
			self.qbits = [q for q in qbits]
		def addtocanvas(self,canvas):
			canvas._add_boxed(self.qbits,self.name, self.cbit_cond)
			return self
		def check_qbit_args(self,nqbits):
			r,c = self.opMatrix.shape
			if 2**len(self.qbits) != r:
				return False
			return self.varqbit_args(nqbits,1)
		# INHERIT def realign(self,newseq):
		# INHERIT def __str__(self):
	return CUSTOM

def fetch_deprecated_custom_gateclass():
	class CUSTOM(QGate):
		def __init__(self, name, opMatrix, qbits):
			print('CUSTOM gate deprecated, does not support noise_to_each(). Uee QCkt.custom_gate() to register a custom gate.', file=sys.stderr)
			super().__init__()
			self.name = name
			if not gutils.isunitary(opMatrix):
				errmsg = "Custom gate, "+self.name+", operator matrix is not unitary."
				raise QCktException(errmsg)
			self.opMatrix = opMatrix
			self.qbits = qbits
		def addtocanvas(self,canvas):
			canvas._add_boxed(self.qbits,self.name, self.cbit_cond)
			return self
		def check_qbit_args(self,nqbits):
			r,c = self.opMatrix.shape
			if 2**len(self.qbits) != r:
				return False
			return self.varqbit_args(nqbits,1)
		# INHERIT def realign(self,newseq):
		# INHERIT def __str__(self):

	return CUSTOM