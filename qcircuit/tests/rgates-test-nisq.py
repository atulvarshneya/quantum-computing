#!/usr/bin/env python

import numpy as np
import qckt
from qckt.backend import *

theta = 3*np.pi/2

ck = qckt.QCkt(1)
ck.X(0)
ck.H(0)
ck.Probe()
ck.Rx(theta,0)
ck.draw()
job = qckt.Job(ck)
NISQdeb().runjob(job)
print("STATE VECTOR READ OUT")
print(job.get_svec())
print("CREGISTER READ OUT: ",end="")
print()
print(job.get_creg()[0])


ck = qckt.QCkt(1)
ck.X(0)
ck.H(0)
ck.Probe()
ck.Ry(theta,0)
ck.draw()
job = qckt.Job(ck)
NISQdeb().runjob(job)
print("STATE VECTOR READ OUT")
print(job.get_svec())
print("CREGISTER READ OUT: ",end="")
print()
print(job.get_creg()[0])


ck = qckt.QCkt(1)
ck.X(0)
ck.H(0)
ck.Probe()
ck.Rz(theta,0)
ck.draw()
job = qckt.Job(ck)
NISQdeb().runjob(job)
print("STATE VECTOR READ OUT")
print(job.get_svec())
print("CREGISTER READ OUT: ",end="")
print()
print(job.get_creg()[0])

