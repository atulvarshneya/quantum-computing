#!/usr/bin/env python3

class Canvas:

	def __init__(self,circuit):
		self.circuit = circuit
		(self.nqubits, self.nclbits) = self.circuit.get_size()
		self.paper = None
		self.lsb_on_top = True # default is to have LSB on top, MSB at the bottom

	def _initcanvas(self):
		self.paper = [[None]*(self.nqubits*2+2)]
		for i in range(self.nqubits+1):
			self.paper[0][i*2] = "q{0:03d} ".format(i)
			self.paper[0][i*2+1] = "     "
		self.paper[0][self.nqubits*2] = "creg "
		self._extend()
		return self

	def _get1col(self, width=1):
		col = [None]*(self.nqubits*2+2)
		for i in range(self.nqubits+1):
			col[i*2] = "-"*width
			col[i*2+1] = " "*width
		col[self.nqubits*2] = "="*width
		return col

	def _extend(self):
		col = self._get1col(1)
		self.paper.append(col)
		return self

	def _paint(self):
		nrows = len(self.paper)
		ncols = len(self.paper[0])
		for i in range(ncols):
			for j in range(nrows):
				print(self.paper[j][i], end='')
			print()

	def append(self,col):
		list = self.paper
		list.append(col)
		return self

	def draw(self):
		self._initcanvas()
		### run through the circuit
		for g in self.circuit:
			g.addtocanvas(self)
		self._paint()

