#!/usr/bin/python3

import numpy as np
import random as rnd
import types
from copy import deepcopy

import qclib

class QCkt:

	def __init__(self, nq, nc=None, name="QCkt"):
		# nq - number of quantum bits
		# nc - number of classical bits
		if (nc == None):
			nc = nq
		self.nq = nq
		self.nc = nc
		self.name = name
		self.circuit = []
		self.idx = 0 # for iterations

	def __add__(self, otherckt):
		# otherckt - teh ckt to be appended
		print("adding ",self.name, " to ", otherckt.name)

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

	def C(self, ctrl, target):
		self.circuit.append(["C",[ctrl,target]])
		return self
	
	def H(self, qubit):
		self.circuit.append(["H",[qubit]])
		return self

	def X(self, qubit):
		self.circuit.append(["X",[qubit]])
		return self

	def Y(self, qubit):
		self.circuit.append(["Y",[qubit]])
		return self

	def Z(self, qubit):
		self.circuit.append(["Z",[qubit]])
		return self

	def T(self, ctl1, ctl2, target):
		self.circuit.append(["T",[ctl1,ctl2,target]])
		return self

	def M(self, qbits, cbits=None):
		if cbits is None:
			cbits = qbits
		self.circuit.append(["M",[qbits,cbits]])
		return self

class Backend:

	def __init__(self):
		self.circuit = None
		self.cregister = None
		self.state_vector = None
	
	def run(self, circuit):
		self.circuit = circuit
		qc = qclib.qcsim(self.circuit.nq, ncbits=self.circuit.nc)

		### run through the circuit
		for g in self.circuit:
			if g[0] == "C":
				qc.qgate(qc.C(),g[1])
			if g[0] == "H":
				qc.qgate(qc.H(),g[1])
			if g[0] == "X":
				qc.qgate(qc.X(),g[1])
			if g[0] == "Y":
				qc.qgate(qc.Y(),g[1])
			if g[0] == "Z":
				qc.qgate(qc.Z(),g[1])
			if g[0] == "T":
				qc.qgate(qc.T(),g[1])
			if g[0] == "M":
				qc.qmeasure_to_cregister(g[1][0],g[1][1])

		# fetch the last value of the cregister, state_vector
		(self.cregister, self.state_vector) = qc.qsnapshot()

	def get_svec(self):
		return self.state_vector

	def print_svec(self):
		statefmt = "{0:"+"0{0:d}b".format(self.circuit.nq)+"}"
		s = 0
		for i in self.state_vector:
			print(statefmt.format(s), i[0])
			s += 1
	
	def get_creg(self):
		return self.cregister

if __name__ == "__main__":
	# test 01
	qckt1 = QCkt(3,3,name="ckt01")
	qckt2 = QCkt(4,name="ckt02")
	qckt3 = qckt1 + qckt2

	#test 02
	qckt = QCkt(2,2)
	qckt.H(0)
	qckt.C(0,1)
	qckt.M([0,1])

	bk = Backend()
	bk.run(qckt)
	bk.print_svec()

	print(bk.get_creg())
