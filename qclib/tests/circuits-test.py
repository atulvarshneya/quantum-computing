#!/usr/lib/python3

import qcckt as qk

ckt1 = qk.QCkt(4,4)

ckt1.X(0)
ckt1.C(0,1)
ckt1.H(1)
ckt1.X(2)
ckt1.T(2,0,1)
ckt1.Border()

ckt2 = qk.QCkt(6,6)
ckt2.Y(4)
ckt2.Z(5)
ckt2.Border()

ckt1 = ckt1.realign(6,6,[3,2,1,0])

ckt3 = ckt1 + ckt2
ckt3.T(4,5,3)
ckt3.M([3,4,5],[3,4,5])

ckt3.draw()

bk = qk.Backend()
bk.run(ckt3, qtrace=False)
print("READ OUT STATE VECTOR: ")
print(bk.get_svec())
res = bk.get_creg()
print("READ OUT CREGISTER: ", end="")
print(res)
