#!/usr/bin/env python3

from Canvas import *
from Gates import *
import qsim
import numpy as np

class QCkt:
	
	def __init__(self, nqubits, nclbits=None, name="QCkt"):
		# nq - number of quantum bits
		# nc - number of classical bits
		if (nclbits == None):
			nclbits = nqubits
		self.nqubits = nqubits
		self.nclbits = nclbits
		self.circuit = []
		self.name = name
		self.canvas = Canvas(self)

		self.X = GateWrapper(self.circuit,X).addGate
		self.Y = GateWrapper(self.circuit,Y).addGate
		self.Z = GateWrapper(self.circuit,Z).addGate
		self.H = GateWrapper(self.circuit,H).addGate
		self.CX = GateWrapper(self.circuit,CX).addGate
		self.T = GateWrapper(self.circuit,T).addGate
		self.M = GateWrapper(self.circuit,M).addGate
		self.Border = GateWrapper(self.circuit,Border).addGate
		self.QFT = GateWrapper(self.circuit,QFT).addGate
		self.RND = GateWrapper(self.circuit,RND).addGate

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

	def append(self, otherckt):
		# otherckt - the ckt to be appended
		nq = max(self.nqubits, otherckt.nqubits)
		nc = max(self.nclbits, otherckt.nclbits)
		self.nqubits = nq
		self.nclbits = nc
		for g in otherckt.circuit:
			self.circuit.append(g)
		return self

	def realign(self,newnq,newnc,inpqubits): # change the qubits order to a different order
		# newq and newc are the new sizes of the qubits register and clbits register
		# inpqubits gives the new positions of the qubits
		# i.e., [3,0,2,1] means old 0 to new 3, old 1 to new 0, old 2, to new 2, old 3 to new 1
		if self.nqubits != len(inpqubits):
			errmsg = "Error: error aligning qubits, number of qubits do not match"
			raise qsim.QClibError(errmsg)
		newckt = QCkt(newnq, newnc)
		for g in self.circuit:
			galigned = g.realign(inpqubits)
			newckt.circuit.append(galigned)
		return newckt

	def get_size(self):
		return self.nqubits, self.nclbits

	def draw(self):
		self.canvas.draw()

class GateWrapper:
	def __init__(self, circuit, gateCls):
		self.circuit = circuit
		self.GateCls = gateCls
	def addGate(self, *args, **kwargs):
		gate = self.GateCls(*args, **kwargs)
		self.circuit.append(gate)

		
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

		return self

	def get_svec(self):
		return self.result.state_vector

	def get_creg(self):
		return self.result.cregister


class _Cregister:

	def __init__(self):
		self.value = None

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
		if v == True:
			self.verbosity = True
		else:
			self.verbosity = False
		return self


class Result:

	def __init__(self):
		self.cregister = _Cregister()
		self.state_vector = _StateVector()


if __name__ == "__main__":
	c1 = QCkt(4)
	c1.X(0)
	c1.draw()
	bk = Backend()
	bk.run(c1,qtrace=True)
	print("RESULT STATE VECTOR:")
	print(bk.get_svec())

	c1 = QCkt(4)
	c1.X(0)
	c1.Y(0)
	c1.X(1)
	c1.Z(1)
	c1.draw()
	bk = Backend()
	bk.run(c1,qtrace=True)
	print("RESULT STATE VECTOR:")
	print(bk.get_svec())

	c1 = QCkt(4)
	c1.H(0)
	c1.CX(0,2)
	c1.draw()
	bk = Backend()
	bk.run(c1,qtrace=True)
	print("RESULT STATE VECTOR:")
	print(bk.get_svec())

	c1 = QCkt(8)
	c1.QFT([6,5,4,3,2,1])
	c1.draw()
	bk = Backend()
	bk.run(c1,qtrace=True)
	print("RESULT STATE VECTOR:")
	print(bk.get_svec())
