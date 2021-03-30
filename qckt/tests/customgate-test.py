import qckt
import numpy as np

ck = qckt.QCkt(4)
opmat = np.matrix([
	[1,0,0,0],
	[0,1,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
ck.custom_gate("CNOT",opmat)


ck.H(0)
ck.CNOT([0,2])
ck.draw()
inpqubits = [3,1,2,0]
ck = ck.realign(4,4,inpqubits)
print("realigned with:",inpqubits)
ck.draw()
bk = qckt.Backend()
bk.run(ck,qtrace=True)
