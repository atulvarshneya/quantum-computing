#!/usr/bin/env python

import qckt as qk
from QSystems import *
from Job import Job

ckt1 = qk.QCkt(4,4)

ckt1.X(0)
ckt1.CX(0,1)
ckt1.H(1)
ckt1.X(2)
ckt1.CCX(2,0,1)
ckt1.Border()

ckt2 = qk.QCkt(6,6)
ckt2.Y(4)
ckt2.Z(5)
ckt2.Border()

ckt1 = ckt1.realign(6,6,[0,1,2,3])

ckt3 = ckt1.append(ckt2)
ckt3.CCX(4,5,3)
ckt3.M([3,4,5],[3,4,5])

ckt3.draw()

job = Job(ckt3, qtrace=False)
bk = NISQdeb()
bk.runjob(job)
print("READ OUT STATE VECTOR: ")
print(job.get_svec())
res = job.get_creg()[0]
print("READ OUT CREGISTER: ", end="")
print(res)
