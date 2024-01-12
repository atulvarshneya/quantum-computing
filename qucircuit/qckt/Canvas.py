#!/usr/bin/env python3

import qckt.Gates

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

	def _add_simple(self,qbit,symbol,ccond=None):
		if issubclass(type(qbit),list):
			return self._add_multiple(qbit,symbol,ccond)
		else:
			ncols = len(symbol) + 2
			col = self._get1col(ncols)
			col[2*qbit] = "[" + symbol + "]"
			if ccond is not None:
				st = qbit
				for i in range(st,self.nqubits):
					col[i*2+1] = ':' + col[i*2+1][1:]
				tag = f'{ccond[0]}'
				col[2*self.nqubits] = tag + col[2*self.nqubits][len(tag):]
			self._append(col)
			self._extend()
			return self

	def _add_multiple(self,qbits,symbol,ccond=None):
		ncols = len(symbol) + 2
		col = self._get1col(ncols)
		for i in range(len(qbits)):
			col[2*qbits[i]] = "[" + symbol + "]"
		if ccond is not None:
			st = min(qbits)
			for i in range(st,self.nqubits):
				col[i*2+1] = ':' + col[i*2+1][1:]
			tag = f'{ccond[0]}'
			col[2*self.nqubits] = tag + col[2*self.nqubits][len(tag):]
		self._append(col)
		self._extend()
		return self

	def _add_connected(self,qbits,symbols,ccond=None):
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
		if ccond is not None:
			for i in range(st,self.nqubits):
				col[i*2+1] = ':' + col[i*2+1][1:]
			tag = f'{ccond[0]}'
			col[2*self.nqubits] = tag + col[2*self.nqubits][len(tag):]
		self._append(col)
		self._extend()
		return self

	def _add_boxed(self,qbits,symbol,ccond=None):
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
		if ccond is not None:
			for i in range(en,self.nqubits):
				col[i*2+1] = ':' + col[i*2+1][1:]
			tag = f'{ccond[0]}'
			col[2*self.nqubits] = tag + col[2*self.nqubits][len(tag):]
		self._append(col)
		self._extend()
		return self

	def _paint(self):
		if self.circuit.name is not None:
			print(self.circuit.name)
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

	def draw(self,show_noise=True):
		self._initcanvas()
		### draw the init noise
		noise_profile = self.circuit.noise_profile
		if (noise_profile is not None) and show_noise:
			if noise_profile.noise_chan_init is not None:
				init_noise_list = []
				for op in noise_profile.noise_chan_init:
					init_noise_list.append(op.name)
				circuit_qubits = [i for i in range(self.circuit.nqubits)]
				init_noise_label = 'INIT:'+','.join(init_noise_list)
				self._add_simple(circuit_qubits,init_noise_label)
		### run through the circuit
		for g in self.circuit:
			if (type(g) is not qckt.Gates.NOISE) or show_noise:
				g.addtocanvas(self)
			if show_noise:
				g.addtocanvas_gatenoise(self, noise_profile=self.circuit.noise_profile, noise_profile_gates=self.circuit.noise_profile_gates)
				if type(g) is not qckt.Gates.NOISE:
					if noise_profile is not None and noise_profile.noise_chan_allsteps is not None and g.is_noise_step():
						for kop,qbt in noise_profile.noise_chan_allsteps:
							self._add_simple(qbt, "AS:"+kop.name)
		self._paint()

