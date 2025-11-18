#!/usr/bin/env python

# Standard teleportation protocol

import qckt
from qckt.backend import Qdeb

ckt = qckt.QCkt(3,3)
ckt.RND(2)
ckt.Border()
ckt.Probe()
ckt.H(0)
ckt.CX(0,1)
ckt.Border()
ckt.CX(2,1)
ckt.H(2)
ckt.M([1])
ckt.M([2])
ckt.X(0).ifcbit(1,1)
ckt.Z(0).ifcbit(2,1)
ckt.Probe()

ckt.draw()

job = qckt.Job(ckt,qtrace=False, verbose=False)
bk = Qdeb()
bk.runjob(job)
print('READ OUT RUNSTATS')
job.print_runstats()
