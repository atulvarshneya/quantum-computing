import numpy as np
import qckt
from qckt import QCktException
from qckt.backend import *

opmat = np.matrix([
	[1,0,0,0],
	[0,1,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
qckt.define_gate("CNOT",opmat)

ck = qckt.QCkt(4)
ck.H(0)
ck.CNOT(0,2)
ck.draw()
inpqubits = [3,1,2,0]
ck = ck.realign(4,4,inpqubits)
print("realigned with:",inpqubits)
ck.draw()

## by appending circuits, the custom gates definitions are available to the new circuit
ckt = qckt.QCkt(6)
ckt = ckt.append(ck)
ckt = ckt.append(ck)
ckt.CNOT(1,3)
ckt.draw()
job = qckt.Job(ckt,qtrace=True)
Qdeb().runjob(job)

print("==Unitary test=======================")
opmatx = np.matrix([
	[2,0,0,0],
	[0,2,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
try:
	qckt.define_gate("CuCXx",opmatx)
except QCktException as e:
	print(e)

qckt.define_gate("CuCX",opmat)
ckt = qckt.QCkt(6)
ckt.CuCX(1,3)
ckt.draw()
job = qckt.Job(ckt,qtrace=True)
Qdeb().runjob(job)
