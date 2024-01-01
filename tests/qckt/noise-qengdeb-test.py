#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns

# added noise model, but using Qdeb
print('added noise model, but using Qdeb')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.KrausOperatorSequence(ns.phase_flip(probability=0.1)))
# ck.H([2])
ck.M([2,1,0])
noise_model = ns.NoiseModel(
	kraus_opseq_init=ns.KrausOperatorSequence(ns.phase_flip(probability=0.2)),
	kraus_opseq_allgates=ns.KrausOperatorSequence(ns.depolarizing(probability=0.1)),
	kraus_opseq_qubits=ns.KrausOperatorApplierSequense(ns.KrausOperatorSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.add_noise_model(noise_model=noise_model)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.Qdeb()
bk.runjob(job)
svec = job.get_svec()
creg = job.get_creg()
cnum = job.get_counts()
print("READ OUT STATE VECTOR: ")
print(svec)
print("READ OUT CREG: ")
print(creg[0])
print(cnum)
print()

# added noise model, but using Qeng
print('added noise model, but using Qeng')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.KrausOperatorSequence(ns.phase_flip(probability=0.1)))
# ck.H([2])
ck.M([2,1,0])
noise_model = ns.NoiseModel(
	kraus_opseq_init=ns.KrausOperatorSequence(ns.phase_flip(probability=0.2)),
	kraus_opseq_allgates=ns.KrausOperatorSequence(ns.depolarizing(probability=0.1)),
	kraus_opseq_qubits=ns.KrausOperatorApplierSequense(ns.KrausOperatorSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.add_noise_model(noise_model=noise_model)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True, shots=100)
bk = bknd.Qeng()
bk.runjob(job)
svec = job.get_svec()
creg = job.get_creg()
cnum = job.get_counts()
print("READ OUT STATE VECTOR: ")
print(svec)
print("READ OUT CREG: ")
print(creg[0])
print(cnum)
