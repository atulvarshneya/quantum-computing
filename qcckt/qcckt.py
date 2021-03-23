#!/usr/bin/python3

import qclib
import numpy as np

class QCkt:

	def __init__(self, nqubits, nclbits=None, name="QCkt"):
		# nq - number of quantum bits
		# nc - number of classical bits
		if (nclbits == None):
			nclbits = nqubits
		self.nqubits = nqubits
		self.nclbits = nclbits
		self.name = name
		self.circuit = []
		self.idx = 0 # for iterations

	def __add__(self, otherckt):
		# otherckt - the ckt to be appended
		print("Warning: Operator + is deprecated. Use qckt.append(qckt) instead.")
		return self.append(otherckt)

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

	def get_size(self):
		return self.nqubits, self.nclbits

	def realign(self,newnq,newnc,inpqubits): # change the qubits order to a different order
		if self.nqubits != len(inpqubits):
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

	def CX(self, ctrl, target):
		self.circuit.append(["CX",[ctrl,target]])
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

	def M(self, qubitslist, clbitslist=None):
		if clbitslist is None:
			clbitslist = qubitslist
		self.circuit.append(["M",[qubitslist,clbitslist]])
		return self

	def Border(self):
		self.circuit.append(["BORDER"])

	##
	## Draw related ethods
	##
	
	def _initcanvas(self):
		canvas = [[" "]*(self.nqubits*2+2)]
		for i in range(self.nqubits*2+2):
			if i%2 == 0:
				canvas[0][i] = "q{0:03d} ".format(i//2)
			else:
				canvas[0][i] = "     "
		canvas[0][self.nqubits*2] = "creg "
		self._extend(canvas)
		return canvas

	def _get1col(self):
		col = [" "]*(self.nqubits*2+2)
		for i in range(self.nqubits*2+2):
			if i%2 == 0:
				col[i] = "-"
			else:
				col[i] = " "
		col[self.nqubits*2] = "="
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

	def _addCX(self, canvas, qbits):
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
			en = self.nqubits*2
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
		en = (self.nqubits+1)*2
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
			if g[0] == "CX":
				self._addCX(canvas,g[1])
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

class Cregister:

	def __init__(self):
		self.value = None

	def __str__(self):
		creg_str = ""
		for i in reversed(range(len(self.value))): # reversed because creg[0] is LSB
			creg_str = creg_str + "{0:01b}".format(self.value[i])
		creg_str = creg_str + "\n"
		return creg_str

class StateVector:

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
				svec_str = svec_str + statefmt.format(s) + "  " + str(i[0]) + "\n"
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
		self.cregister = Cregister()
		self.state_vector = StateVector()


class Backend:

	def __init__(self):
		self.circuit = None
		self.result = Result()

	def run(self, circuit, initstate=None, prepqubits=None, qtrace=False):
		self.circuit = circuit
		qc = qclib.qcsim(self.circuit.nqubits, ncbits=self.circuit.nclbits, initstate=initstate, prepqubits=prepqubits, qtrace=qtrace)

		### run through the circuit
		for g in self.circuit:
			if g[0] == "CX":
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
		(self.result.cregister.value, self.result.state_vector.value) = qc.qsnapshot()

		return self

	def get_svec(self):
		return self.result.state_vector

	def get_creg(self):
		return self.result.cregister


if __name__ == "__main__":
	pass
