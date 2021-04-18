#!/usr/bin/python3

from qException import QCktException

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
class QRegister(Register):
	pass
class CRegister(Register):
	pass

def placement(*regs):
	qbitplaced = []
	cbitplaced = []
	qbitsz = None
	cbitsz = None
	for r in reversed(regs):
		if type(r) is QRegister:
			qbitsz = qbitsz + len(r) if qbitsz is not None else len(r)
			r.placeMSB(qbitsz - 1)
			qbitplaced = r[:] + qbitplaced
		elif type(r) is CRegister:
			cbitsz = cbitsz + len(r) if cbitsz is not None else len(r)
			r.placeMSB(cbitsz - 1)
			cbitplaced = r[:] + cbitplaced
		else:
			raise QCktException("placement not supported for type:"+type(r).__name__)
	return qbitsz,cbitsz,qbitplaced,cbitplaced
