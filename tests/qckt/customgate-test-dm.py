import numpy as np
import qckt
from qckt import QCktException
from qckt.backend import *

ck = qckt.QCkt(4)
opmat = np.matrix([
	[1,0,0,0],
	[0,1,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)


ck.H(0)
ck.custom_gate("CNOT",opmat)
ck.CNOT(0,2)
ck.draw()
inpqubits = [3,1,2,0]
ck = ck.realign(4,4,inpqubits)
print("realigned with:",inpqubits)
ck.draw()

## by appending circuits, the custom gates definitions are inherited by the new circuit
ckt = qckt.QCkt(6)
ckt = ckt.append(ck)
ckt = ckt.append(ck)
ckt.custom_gate("CNOT",opmat)
ckt.CNOT(1,3)
ckt.draw()
job = qckt.Job(ckt,qtrace=True)
DMQdeb().runjob(job)

## by appending circuits, the custom gates definitions are inherited by the new circuit
print("==Direct CUSTOM gate=======================")
opmatx = np.matrix([
	[2,0,0,0],
	[0,2,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
ckt = qckt.QCkt(6)
ckt.custom_gate("CuCX",opmat)
ckt.CuCX(1,3)
try:
	ckt.custom_gate("CuCXx",opmatx)
	# ckt.CuCXx(1,3)
except QCktException as e:
	print(e)
ckt.draw()
job = qckt.Job(ckt,qtrace=True)
DMQdeb().runjob(job)
