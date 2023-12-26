#!/usr/bin/env python

import qckt
from qckt.backend import *
import qckt.noisemodel as ns

cnotckt = qckt.QCkt(2, 2)

cnotckt.H([0])
cnotckt.CX(0,1)
cnotckt.M([0,1],[0,1])

cnotckt.draw()

noise_model = ns.NoiseModel(kraus_opseq_allgates=ns.KrausOperatorSequence(ns.bit_flip(0.1)))
cnotckt.add_noise_model(noise_model=noise_model)

job = qckt.Job(cnotckt, shots=1000)

print('Backends:',qsimSvc().listInstances())
bk = qsimSvc().getInstance('nisqsim-eng') # NISQeng()
bk.runjob(job)
print()
print("READ OUT STATE VECTOR: ")
print(job.get_svec())
print("READ OUT CREGISTER: ", end="")
print( job.get_creg()[0])
job.plot_counts()
