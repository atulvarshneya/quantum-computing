#!/usr/bin/env python3

import qckt.Canvas as cnv
import qckt.Gates as gts
import qckt.gatesutils as gutils
from qckt.qException import QCktException
import qsim
import numpy as np

class GateWrapper:
	def __init__(self, qckt, gateCls):
		self.qckt = qckt
		self.GateCls = gateCls
	def __call__(self, *args, **kwargs):
		gateObj = self.GateCls(*args, **kwargs)
		self.qckt.circuit.append(gateObj)
		if gateObj.check_qbit_args(self.qckt.nqubits) == False:
			errmsg = "Error: qubit arguments incorrect. " + gateObj.name + str(gateObj.qbits)
			raise QCktException(errmsg)
		return self.qckt

class QCkt:

	def __init__(self, nqubits, nclbits=0, name=None):
		self.nqubits = nqubits
		self.nclbits = nclbits
		self.circuit = []
		self.name = name
		self.canvas = cnv.Canvas(self)

		for gclass in gts.GatesList:
			self._registerGate(gclass.__name__, GateWrapper(self,gclass))

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

	def _registerGate(self, gatename, addgateObj):
		setattr(self,gatename,addgateObj)

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

	def assemble(self):
		assembled = []
		for gt in self.circuit:
			assembled.append(gt.assemble())
		return assembled

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

if __name__ == "__main__":
	pass
