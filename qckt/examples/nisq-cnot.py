#!/usr/bin/env python

import qckt
from QSystems import *
from Job import Job

cnotckt = qckt.QCkt(2, 2)

cnotckt.H([0])
cnotckt.CX(0,1)
cnotckt.M([0,1],[0,1])

cnotckt.draw()

noise_profile = {'profile_id':'BitFlip', 'p1':0.05, 'p2':0.05, 'p3':0.05}
job = Job(cnotckt, noise_profile=noise_profile, shots=1000)
bk = NISQeng()
bk.runjob(job)
print()
print("READ OUT STATE VECTOR: ")
print(job.get_svec())
print("READ OUT CREGISTER: ", end="")
print( job.get_creg()[0])
job.plot_counts()
