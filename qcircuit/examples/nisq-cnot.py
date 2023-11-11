#!/usr/bin/env python

import qckt
from qckt.backend import *

cnotckt = qckt.QCkt(2, 2)

cnotckt.H([0])
cnotckt.CX(0,1)
cnotckt.M([0,1],[0,1])

cnotckt.draw()

noise_profile = {'profile_id':'BitFlip', 'p1':0.05}
job = qckt.Job(cnotckt, noise_profile=noise_profile, shots=1000)

print('Backends:',qsimSvc().listInstances())
bk = qsimSvc().getInstance('nisqsim-eng') # NISQeng()
bk.runjob(job)
print()
print("READ OUT STATE VECTOR: ")
print(job.get_svec())
print("READ OUT CREGISTER: ", end="")
print( job.get_creg()[0])
job.plot_counts()
