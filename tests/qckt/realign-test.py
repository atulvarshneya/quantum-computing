import qckt
from qckt.backend import *

ck = qckt.QCkt(4)
ck.X(0)
ck.H(1)
ck.CX(3,2)
ck.draw()
inpqubits = [4,5,2,3]
ck = ck.realign(6,6,inpqubits)
print("Realigned with:",inpqubits)
ck.draw()

job = qckt.Job(ck,qtrace=True)
bk = Qdeb()
bk.runjob(job)
print()
print("STATE VECTOR READ OUT")
print(job.get_svec())
print("CREGISTER READ OUT")
print(job.get_creg())

