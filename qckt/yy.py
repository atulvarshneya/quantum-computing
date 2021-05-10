#!/usr/bin/python3

import qckt
from Job import *
from QSystems import *

ck = qckt.QCkt(4,4)
ck.H(0)
ck.CX(0,1)
ck.Border()
ck.X([2,3])
ck.H([2,3])
ck.Border()
ck.M([1,0],[1,0])
# ck.Probe("point 1")
ck.draw()

bk = Backend()
bk.run(ck,qtrace=False)
print(bk.get_creg())
print(bk.get_svec())
