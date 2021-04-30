#!/usr/bin/env python3

import Canvas as cnv
import Gates as gts
import GatesUtils as gutils
import qsim
import numpy as np
from qException import QCktException

class GateWrapper:
	def __init__(self, qckt, gateCls):
		self.qckt = qckt
		self.GateCls = gateCls
	def addGate(self, *args, **kwargs):
		gate = self.GateCls(*args, **kwargs)
		self.qckt.circuit.append(gate)
		if gate.check_qbit_args(self.qckt.nqubits) == False:
			errmsg = "Error: qubit arguments incorrect. " + gate.name + str(gate.qbits)
			raise QCktException(errmsg)
		return self.qckt

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

		for gclass in gts.GatesList:
			self._registerGate(gclass.__name__, GateWrapper(self,gclass).addGate)

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

	def append(self, otherckt):
		# otherckt - the ckt to be appended
		nq = max(self.nqubits, otherckt.nqubits)
		nc = max(self.nclbits, otherckt.nclbits)
		newckt = QCkt(nq,nc,name=self.name)

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
			raise QCktException(errmsg)
		newckt = QCkt(newnq, newnc, name=self.name)
		for g in self.circuit:
			galigned = g.realign(inpqubits)
			newckt.circuit.append(galigned)
		return newckt

	def to_opMatrix(self):
		oplist = []
		for q in self.circuit:
			op = q.to_fullmatrix(self.nqubits)
			if op is not None: ## Border, Probe gates return None
				oplist.append(op)
		opmat = gutils.combine_seq(oplist)
		return opmat

	def get_size(self):
		return self.nqubits, self.nclbits

	def draw(self):
		self.canvas.draw()

	def list(self):
		if self.name is not None:
			print(self.name)
		for g in self.circuit:
			print(g)

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
		(self.result.cregister.value, self.result.state_vector.value) = (creg,svec)
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
			if self.verbosity or np.absolute(i) > 10**(-6):
				svec_str = svec_str + statefmt.format(s) + "  " + "{:.8f}".format(i) + "\n"
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
	pass
