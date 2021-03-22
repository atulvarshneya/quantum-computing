#!/usr/bin/python3

import qclib
import numpy as np

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
		# otherckt - the ckt to be appended
		nq = max(self.nq, otherckt.nq)
		self.nq = nq
		for g in otherckt.circuit:
			self.circuit.append(g)
		return self

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

	def realign(self,newnq,newnc,inpqubits): # change the qubits order to a different order
		if self.nq != len(inpqubits):
			errormsg = "Error: error aligning qubits, number of qubits do not match"
			raise qclib.QClibError(errmsg)
		newckt = QCkt(newnq, newnc)
		for g in self.circuit:
			if g[0] == "M":
				qbits = g[1][0]
				cbits = g[1][1]
				nqbits = self._reorderlist(qbits,inpqubits)
				ncbits = self._reorderlist(cbits,inpqubits)
				newckt.circuit.append([g[0],[nqbits,ncbits]])
			elif g[0] == "BORDER":
				newckt.circuit.append([g[0]])
			else:
				qbits = g[1]
				nqbits = self._reorderlist(qbits,inpqubits)
				newckt.circuit.append([g[0],nqbits])
		return newckt

	def _reorderlist(self,oseq,nseq):
		newseq = []
		for i in oseq:
			newseq.append(nseq[i])
		return newseq

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

	def Border(self):
		self.circuit.append(["BORDER"])

	##
	## Draw related ethods
	##
	
	def _initcanvas(self):
		canvas = [[" "]*(self.nq*2+2)]
		for i in range(self.nq*2+2):
			if i%2 == 0:
				canvas[0][i] = "q{0:03d} ".format(i//2)
			else:
				canvas[0][i] = "     "
		canvas[0][self.nq*2] = "creg "
		self._extend(canvas)
		return canvas

	def _get1col(self):
		col = [" "]*(self.nq*2+2)
		for i in range(self.nq*2+2):
			if i%2 == 0:
				col[i] = "-"
			else:
				col[i] = " "
		col[self.nq*2] = "="
		return col
    
	def _extend(self, canvas):
		col = self._get1col()
		canvas.append(col)
		return canvas

	def _addX(self, canvas, qbits):
		col = self._get1col()
		col[qbits[0]*2] = "["
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "X"
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "]"
		canvas.append(col)
		canvas = self._extend(canvas)
		return canvas

	def _addY(self, canvas, qbits):
		col = self._get1col()
		col[qbits[0]*2] = "["
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "Y"
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "]"
		canvas.append(col)
		canvas = self._extend(canvas)
		return canvas

	def _addZ(self, canvas, qbits):
		col = self._get1col()
		col[qbits[0]*2] = "["
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "Z"
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "]"
		canvas.append(col)
		canvas = self._extend(canvas)
		return canvas

	def _addC(self, canvas, qbits):
		col = self._get1col()
		col[qbits[0]*2] = "["
		col[qbits[1]*2] = "["
		canvas.append(col)
		col = self._get1col()
		st = min(qbits[0], qbits[1])*2
		en = max(qbits[0], qbits[1])*2
		for i in range(en-st-1):
			col[i+st+1] = "|"
		col[qbits[0]*2] = "."
		col[qbits[1]*2] = "X"
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "]"
		col[qbits[1]*2] = "]"
		canvas.append(col)
		canvas = self._extend(canvas)
		return canvas

	def _addT(self, canvas, qbits):
		col = self._get1col()
		col[qbits[0]*2] = "["
		col[qbits[1]*2] = "["
		col[qbits[2]*2] = "["
		canvas.append(col)
		col = self._get1col()
		st = min(qbits[0], qbits[1], qbits[2])*2
		en = max(qbits[0], qbits[1], qbits[2])*2
		for i in range(en-st-1):
			col[i+st+1] = "|"
		col[qbits[0]*2] = "."
		col[qbits[1]*2] = "."
		col[qbits[2]*2] = "X"
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "]"
		col[qbits[1]*2] = "]"
		col[qbits[2]*2] = "]"
		canvas.append(col)
		canvas = self._extend(canvas)
		return canvas

	def _addH(self, canvas, qbits):
		col = self._get1col()
		col[qbits[0]*2] = "["
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "H"
		canvas.append(col)
		col = self._get1col()
		col[qbits[0]*2] = "]"
		canvas.append(col)
		canvas = self._extend(canvas)
		return canvas

	def _addM(self, canvas, qbits):
		for qb in qbits:
			col = self._get1col()
			col[qb*2] = "["
			canvas.append(col)
			col = self._get1col()
			col[qb*2] = "M"
			st = qb*2
			en = self.nq*2
			for i in range(en-st-1):
				col[i+st+1] = "|"
			col[en] = "v"
			canvas.append(col)
			col = self._get1col()
			col[qb*2] = "]"
			canvas.append(col)
			canvas = self._extend(canvas)
		return canvas

	def _addBORDER(self, canvas):
		canvas = self._extend(canvas)
		col = self._get1col()
		en = (self.nq+1)*2
		for i in range(en):
			col[i] = "#"
		canvas.append(col)
		canvas = self._extend(canvas)

	def _paint(self, canvas):
		nrows = len(canvas)
		ncols = len(canvas[0])
		for i in range(ncols):
			for j in range(nrows):
				print(canvas[j][i], end='')
			print()

	def draw(self):
		canvas = self._initcanvas()
		### run through the circuit
		for g in self.circuit:
			if g[0] == "C":
				self._addC(canvas,g[1])
			if g[0] == "H":
				self._addH(canvas,g[1])
			if g[0] == "X":
				self._addX(canvas,g[1])
			if g[0] == "Y":
				self._addY(canvas,g[1])
			if g[0] == "Z":
				self._addZ(canvas,g[1])
			if g[0] == "T":
				self._addT(canvas,g[1])
			if g[0] == "M":
				self._addM(canvas,g[1][0])
			if g[0] == "BORDER":
				self._addBORDER(canvas)
		self._paint(canvas)

class Result:
	def __init__(self):
		self.cregister = None
		self.state_vector = None


class Backend:

	def __init__(self):
		self.circuit = None
		self.result = Result()

	def run(self, circuit, qtrace=False):
		self.circuit = circuit
		qc = qclib.qcsim(self.circuit.nq, ncbits=self.circuit.nc, qtrace=qtrace)

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
				qc.qmeasure(g[1][0],cbit_list=g[1][1])

		# fetch the last value of the cregister, state_vector
		(self.result.cregister, self.result.state_vector) = qc.qsnapshot()

	def get_svec(self):
		return self.result.state_vector

	def print_svec(self):
		statefmt = "{0:"+"0{0:d}b".format(self.circuit.nq)+"}"
		s = 0
		for i in self.result.state_vector:
			if np.absolute(i[0]) > 10**(-6):
				print(statefmt.format(s), i[0])
			s += 1
	
	def get_creg(self):
		return self.result.cregister

if __name__ == "__main__":
	pass
