#!/usr/bin/env python3

class GateWrapper:
	def __init__(self, circuit, gateCls):
		self.circuit = circuit
		self.GateCls = gateCls
	def addGate(self, *args, **kwargs):
		gate = self.GateCls(*args, **kwargs)
		self.circuit.append(gate)

class QGate:
	def __init__(self):
		pass
	def _reorderlist(self,oseq,nseq):
		newseq = []
		nqbits = len(nseq)
		for i in oseq:
			newseq.append(nseq[nqbits-i-1])
		return newseq

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

class T(QGate):

	def __init__(self, control1, control2, target):
		self.qbits = [control1, control2, target]

	def addtocanvas(self,canvas):
		col = canvas._get1col(3)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "-|-"
			col[i*2+1] = " | "
		col[self.qbits[0]*2] = "[.]"
		col[self.qbits[1]*2] = "[.]"        
		col[self.qbits[2]*2] = "[X]"        
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "T:"+str(self.qbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.T(),self.qbits)

class M(QGate):

	def __init__(self, qubitslist, clbitslist=None):
		if clbitslist is None:
			clbitslist = qubitslist
		if (type(qubitslist) != list) or (type(clbitslist) != list):
			errmsg = "Error: M gate requires a list of qubits and optionally a list of classical bits as arguments"
			raise qsim.QSimError(errmsg)
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

class RND(QGate):
	def __init__(self, qbit):
		self.qbits = [qbit]
	
	def addtocanvas(self,canvas):
		col = canvas._get1col(5)
		col[self.qbits[0]*2] = "[RND]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "RND:"+str(self.qbits)
	
	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.RND(),self.qbits)

class ROT(QGate):
	def __init__(self, phi, qbit):
		self.qbits = [qbit]
		self.phi = phi

	def addtocanvas(self,canvas):
		col = canvas._get1col(5)
		col[self.qbits[0]*2] = "[ROT]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "ROT("+"{:f}".format(self.phi)+"):"+str(self.qbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.Rphi(self.phi),self.qbits)

class Rk(QGate):
	def __init__(self, k, qbit):
		self.qbits = [qbit]
		self.k = k

	def addtocanvas(self,canvas):
		col = canvas._get1col(4)
		col[self.qbits[0]*2] = "[Rk]"
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return "Rk("+"{:d}".format(self.k)+"):"+str(self.qbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate(qc.Rk(self.k),self.qbits)

GatesList = [X,Y,Z,H,CX,T,M,Border,QFT,RND,ROT,Rk]

###################################################
### Support for Custom Gates
###################################################

class CustomGateWrapper:
	def __init__(self, circuit, gatename, opMatrix):
		self.gatename = gatename
		self.opMatrix = opMatrix
		self.circuit = circuit
	def addGate(self, qbits):
		qbitsList = qbits
		if type(qbitsList).__name__ != 'list':
			qbitsList = [qbits]
		gate = CustomGate(self.gatename, self.opMatrix, qbitsList)
		self.circuit.append(gate)

class CustomGate(QGate):

	def __init__(self, gatename, opMatrix, qbits):
		self.gatename = gatename
		self.opMatrix = opMatrix
		self.qbits = qbits

	def addtocanvas(self,canvas):
		ncols = len(self.gatename) + 2 # 2 for '[', ']'
		usegname = self.gatename
		if (len(self.qbits) > 1):
			ncols += 2 # for ' M' and ' L' to indicate MSB, LSB
			usegname = self.gatename+"  "
			usegnameM = self.gatename+" M"
			usegnameL = self.gatename+" L"
		col = canvas._get1col(ncols)
		st = min(self.qbits)
		en = max(self.qbits)
		for i in range(st,en):
			col[i*2] = "|"+ "-"*(ncols-2)+"|"
			col[i*2+1] = "|"+ " "*(ncols-2)+"|"
		for q in self.qbits:
			col[q*2] = "["+usegname+"]"
		if len(self.qbits) > 1:
			col[self.qbits[0]*2] = '['+usegnameM+']'
			col[self.qbits[-1]*2] = '['+usegnameL+']'
		canvas.append(col)
		canvas._extend()
		return self

	def realign(self,newseq):
		self.qbits = self._reorderlist(self.qbits,newseq)
		return self

	def __str__(self):
		return self.gatename+":"+str(self.qbits)

	def exec(self,qc):
		# print("exec qc.qgate(",str(self),")")
		qc.qgate([self.gatename,self.opMatrix],self.qbits)

