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

	def _add_simple(self,qbit,symbol):
		if type(qbit) is list:
			return self._add_multiple(qbit,symbol)
		else:
			ncols = len(symbol) + 2
			col = self._get1col(ncols)
			col[2*qbit] = "[" + symbol + "]"
			self._append(col)
			self._extend()
			return self

	def _add_multiple(self,qbits,symbol):
		ncols = len(symbol) + 2
		col = self._get1col(ncols)
		for i in range(len(qbits)):
			col[2*qbits[i]] = "[" + symbol + "]"
		self._append(col)
		self._extend()
		return self

	def _add_connected(self,qbits,symbols):
		ncols = max([len(e) + 2 for e in symbols])
		post = (ncols-1) // 2
		pre = (ncols-1) - post
		col = self._get1col(ncols)
		st = min(qbits)
		en = max(qbits)
		for i in range(st,en):
			col[i*2] = "-"*pre + "|" + "-"*post
			col[i*2+1] = " "*pre + "|" + " "*post
		for i in range(len(qbits)):
			padding = ncols - len(symbols[i]) - 2
			post = padding // 2
			pre = padding - post
			col[2*qbits[i]] = "-"*pre + "[" + symbols[i] + "]" + "-"*post
		self._append(col)
		self._extend()
		return self

	def _add_boxed(self,qbits,symbol):
		ncols =  len(symbol) + 4 # 4 to make space for "[", " M"/" L", "]"
		col = self._get1col(ncols)
		st = min(qbits)
		en = max(qbits)
		for i in range(st,en):
			col[i*2] = "|" + "-"*(ncols - 2) + "|"
			col[i*2+1] = "|" + " "*(ncols - 2) + "|"
		lsb = qbits[-1]
		msb = qbits[0]
		for q in qbits:
			if q == msb:
				col[2*msb] = "[" + symbol + " M]"
			elif q == lsb:
				col[2*lsb] = "[" + symbol + " L]"
			else:
				col[2*q] = "[" + symbol + "  ]"
		self._append(col)
		self._extend()
		return self

	def _paint(self):
		ncols = len(self.paper)
		nrows = len(self.paper[0])
		for i in range(nrows):
			for j in range(ncols):
				print(self.paper[j][i], end='')
			print()

	def _append(self,col):
		list = self.paper
		list.append(col)
		return self

	def draw(self):
		self._initcanvas()
		### run through the circuit
		for g in self.circuit:
			g.addtocanvas(self)
		self._paint()

