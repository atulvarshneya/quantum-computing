#!/usr/bin/env python

import qckt
from qckt.backend import *

ck = qckt.QCkt(4,4)
ck.H(0)
ck.CX(0,1)
ck.Border()
ck.X([2,3])
ck.Border()
# ck.M([1,0],[1,0])
ck.Probe("point 1")
ck.draw()

job = qckt.Job(ck,qtrace=False,shots=5)
bk = DMQdeb().runjob(job)
# bk = DMQeng().runjob(job)
print(job.get_svec())
print(job.get_creg()[0])
