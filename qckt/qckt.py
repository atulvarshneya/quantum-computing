#!/usr/bin/env python3

import Canvas as cnv
import Gates as gts
import qsim
import numpy as np

class QCkt:

	def __init__(self, nqubits, nclbits=None, name=None):
		# nq - number of quantum bits
		# nc - number of classical bits
		if (nclbits is None):
			nclbits = nqubits
		self.nqubits = nqubits
		self.nclbits = nclbits
		self.circuit = []
		self.name = name
		self.canvas = cnv.Canvas(self)

		self.custom_redolog = []
		for gclass in gts.GatesList:
			self._registerGate(gclass.__name__, gts.GateWrapper(self.nqubits,self.circuit,gclass).addGate)

		self.idx = 0 # for iterations

	def __iter__(self):
		self.idx = 0
		return self

	def __next__(self):
		self.idx += 1
		try:
			return self.circuit[self.idx-1]
		except IndexError:
			self.idx = 0
			raise StopIteration  # Done iterating.

	def _registerGate(self, gatename, addgateHandle):
		setattr(self,gatename,addgateHandle)

	def custom_gate(self, gatename, opMatrix):
		if hasattr(self,gatename):
			print("WARNING: Ignored an attempt to overwrite existing QCkt.{:s}.".format(gatename))
		else:
			self.custom_redolog.append([gatename,opMatrix])
			self._registerGate(gatename, gts.CustomGateWrapper(self.nqubits,self.circuit,gatename,opMatrix).addGate)

	def get_custom_redolog(self):
		return self.custom_redolog

	def append(self, otherckt):
		# otherckt - the ckt to be appended
		nq = max(self.nqubits, otherckt.nqubits)
		nc = max(self.nclbits, otherckt.nclbits)
		newckt = QCkt(nq,nc)

		# register custom gates from these circuits to the new circuit
		for cg in self.get_custom_redolog():
			newckt.custom_gate(cg[0], cg[1])
		for cg in otherckt.get_custom_redolog():
			newckt.custom_gate(cg[0], cg[1])

		# copy circuits over to the new circuit
		for g in self.circuit:
			newckt.circuit.append(g)
		for g in otherckt.circuit:
			newckt.circuit.append(g)

		return newckt

	def realign(self,newnq,newnc,inpqubits): # change the qubits order to a different order
		# newq and newc are the new sizes of the qubits register and clbits register
		# inpqubits gives the new positions of the qubits
		# See README.md for details
		if self.nqubits != len(inpqubits):
			errmsg = "Error: error aligning qubits, number of qubits do not match"
			raise qsim.QSimError(errmsg)
		newckt = QCkt(newnq, newnc)
		# register custom gates to the new circuit
		for cg in self.get_custom_redolog():
			newckt.custom_gate(cg[0], cg[1])
		for g in self.circuit:
			galigned = g.realign(inpqubits)
			newckt.circuit.append(galigned)
		return newckt

	def get_size(self):
		return self.nqubits, self.nclbits

	def draw(self):
		self.canvas.draw()

	def list(self):
		if self.name is not None:
			print(self.name)
		for g in self.circuit:
			print(g)
		
######################################################################
## Backend classes ###################################################
######################################################################

class Backend():

	def __init__(self):
		self.circuit = None
		self.result = Result()

	def run(self, circuit, initstate=None, prepqubits=None, qtrace=False):
		self.circuit = circuit
		qc = qsim.QSimulator(self.circuit.nqubits, ncbits=self.circuit.nclbits, initstate=initstate, prepqubits=prepqubits, qtrace=qtrace)
		### run through the circuit
		for g in self.circuit:
			g.exec(qc)
		# fetch the last value of the cregister, state_vector
		(creg, svec) = qc.qsnapshot()
		(self.result.cregister.value, self.result.state_vector.value) = (creg,svec.tolist())
		self.result.cregister.intvalue = 0
		for i in range(len(self.result.cregister.value)):
			self.result.cregister.intvalue = 2 * self.result.cregister.intvalue
			self.result.cregister.intvalue += self.result.cregister.value[i]

		return self

	def get_svec(self):
		return self.result.state_vector

	def get_creg(self):
		return self.result.cregister


class _Cregister:

	def __init__(self):
		self.value = None
		self.intvalue = None

	def __str__(self):
		creg_str = ""
		for i in (range(len(self.value))): # creg[0] is MSB
			creg_str = creg_str + "{0:01b}".format(self.value[i])
		# creg_str = creg_str + "\n"
		return creg_str


class _StateVector:

	def __init__(self):
		self.value = None
		self.verbosity = False

	def __str__(self):
		### wonky way to find number of qubits
		nq = 0
		n = len(self.value) - 1
		while n > 0:
			nq = nq + 1
			n = n >> 1

		statefmt = "{0:"+"0{0:d}b".format(nq)+"}"
		svec_str = ""
		s = 0
		for i in self.value:
			if self.verbosity or np.absolute(i[0]) > 10**(-6):
				svec_str = svec_str + statefmt.format(s) + "  " + "{:.8f}".format(i[0]) + "\n"
			s += 1
		return svec_str

	def verbose(self,v):
		if v is True:
			self.verbosity = True
		else:
			self.verbosity = False
		return self


class Result:

	def __init__(self):
		self.cregister = _Cregister()
		self.state_vector = _StateVector()


if __name__ == "__main__":
	# for i in GatesList:
	#	print(i.__name__)
	import numpy as np
	opMat = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],dtype=complex)

	print("ck1 -----")
	ck1 = QCkt(8)
	ck1.custom_gate("ID",opMat)
	ck1.ID([2,3])
	ck1.draw()

	print("ck2 -----")
	ck2 = QCkt(8)
	ck2.custom_gate("ID",opMat)
	ck2.H(5)
	ck2.draw()

	print("ck3 -----")
	ck3 = ck1.append(ck2)
	ck3.ID([6,7])
	ck3.draw()

	print("ck  -----")
	ck = ck3.realign(8,8,[5,4,7,6,3,2,1,0])
	ck.ID([4,5])
	ck.draw()

	bk = Backend()
	bk.run(ck,qtrace=True)

