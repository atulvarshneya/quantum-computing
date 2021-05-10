import qckt
from QSystems import *

ck = qckt.QCkt(4)
ck.X(0)
ck.H(1)
ck.CX(3,2)
ck.draw()
inpqubits = [4,5,2,3]
ck = ck.realign(6,6,inpqubits)
print("Realigned with:",inpqubits)
ck.draw()
bk = Backend()
bk.run(ck,qtrace=True)
print("STATE VECTOR READ OUT")
print(bk.get_svec())
print("CREGISTER READ OUT")
print(bk.get_creg())

