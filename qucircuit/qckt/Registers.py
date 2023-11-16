#!/usr/bin/python3

from qckt.qException import QCktException

class Register(list):
	def __init__(self,sz):
		super().__init__([None]*sz)
		self.placed = False
	def __getitem__(self,idx):
		if self.placed is False:
			raise QCktException("Attempt to access register qbit ids without placement")
		return super().__getitem__(idx)
	def placeMSB(self,loc):
		for q in range(len(self)):
			self[q] = loc - q
		self.placed = True
		return self
class QRegister(Register):
	pass
class CRegister(Register):
	pass

def placement(*regs):
	qbitplaced = QRegister(0).placeMSB(0) # trick to mark the register 'placed'
	cbitplaced = CRegister(0).placeMSB(0) # trick to mark the register 'placed'
	qbitsz = 0
	cbitsz = 0
	for r in reversed(regs):
		if type(r) is QRegister:
			if r.placed: raise QCktException("Attempt to place already placed QRegister")
			qbitsz = qbitsz + len(r) if qbitsz is not None else len(r)
			r.placeMSB(qbitsz - 1)
			temp = QRegister(0).placeMSB(0) # trick to mark the register 'placed'
			for i in r: temp.append(i)
			temp.extend(qbitplaced)
			qbitplaced = temp
		elif type(r) is CRegister:
			if r.placed: raise QCktException("Attempt to place already placed CRegister")
			cbitsz = cbitsz + len(r) if cbitsz is not None else len(r)
			r.placeMSB(cbitsz - 1)
			temp = CRegister(0).placeMSB(0) # trick to mark the register 'placed'
			for i in r: temp.append(i)
			temp.extend(cbitplaced)
			cbitplaced = temp
		else:
			raise QCktException("placement not supported for type:"+type(r).__name__)
	return qbitsz,cbitsz,qbitplaced,cbitplaced
