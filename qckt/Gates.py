#!/usr/bin/env python3

class QGate:
	def __init__(self):
		pass
	def _reorderlist(self,oseq,nseq):
		newseq = []
		nqbits = len(nseq)
		for i in oseq:
			newseq.append(nseq[nqbits-i-1])
		return newseq
'''
	def _reorderlist(self,oseq,nseq):
		newseq = []
		for i in oseq:
			newseq.append(nseq[i])
		return newseq
'''

class X(QGate):
	def __init__(self, qbit):
		self.qbits = [qbit]
	
	def addtocanvas(self,canvas):
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[X]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "X:"+str(self.qbits)
	
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.X(),self.qbits)

class Y(QGate):
	def __init__(self, qbit):
		self.qbits = [qbit]
	
	def addtocanvas(self,canvas):
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[Y]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "Y:"+str(self.qbits)
	
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.Y(),self.qbits)

class Z(QGate):
	def __init__(self, qbit):
		self.qbits = [qbit]
	
	def addtocanvas(self,canvas):
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[Z]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "Z:"+str(self.qbits)
	
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.Z(),self.qbits)

class H(QGate):
	def __init__(self, qbit):
		self.qbits = [qbit]
	
	def addtocanvas(self,canvas):
		col = canvas._get1col(3)
		col[self.qbits[0]*2] = "[H]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "H:"+str(self.qbits)
	
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.H(),self.qbits)


class CX(QGate):

	def __init__(self, control, target):
		self.qbits = [control, target]

	def addtocanvas(self,canvas):
		col = canvas._get1col(3)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "-|-"
			col[i*2+1] = " | "
		col[self.qbits[0]*2] = "[.]"
		col[self.qbits[1]*2] = "[X]"        
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "CX:"+str(self.qbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.C(),self.qbits)

class QFT(QGate):

	def __init__(self, qbits):
		self.qbits = qbits

	def addtocanvas(self,canvas):
		col = canvas._get1col(7)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "|-----|"
			col[i*2+1] = "|     |"
		for q in self.qbits:
			col[q*2] = "[QFT  ]"
		col[self.qbits[0]*2] = "[QFT M]"
		col[self.qbits[-1]*2] = "[QFT L]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "QFT:"+str(self.qbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.QFT(len(self.qbits)),self.qbits)

class M(QGate):

	def __init__(self, qubitslist, clbitslist=None):
		if clbitslist is None:
			clbitslist = qubitslist
		if (type(qubitslist) != list) or (type(clbitslist) != list):
			errmsg = "Error: M gate requires a list of qubits and optionally a list of classical bits as arguments"
			raise qsim.QClibError(errmsg)
		self.qbits = qubitslist
		self.cbits = clbitslist

	def addtocanvas(self,canvas):
		for qb in self.qbits:
			col = canvas._get1col(3)
			st = qb
			en = len(col)//2 - 1
			for i in range(st,en):
				col[2*i] = "-|-"
				col[2*i+1] = " | "
			col[qb*2] = "[M]"
			col[en*2] = "=v="
			canvas.append(col)
			canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		self.cbits = self._reorderlist(self.cbits,newseq)
		return self

	def __str__(self):
		return "M:"+str(self.qbits)+"-->"+str(self.cbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qmeasure(self.qbits,cbit_list=self.cbits)

class Border(QGate):

	def __init__(self):
		pass

	def addtocanvas(self,canvas):
		canvas._extend()
		col = canvas._get1col(1)
		en = len(col)//2
		for i in range(en):
			col[2*i] = "#"
			col[2*i+1] = "#"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		return self

	def __str__(self):
		return "BORDER"

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		pass

