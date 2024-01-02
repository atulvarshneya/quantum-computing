#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns


print('test 01 - DMQdeb, All KrausOperatorSequence')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.KrausOperatorSequence(ns.phase_flip(probability=0.1)))
ck.H([2])
noise_model = ns.NoiseModel(
	kraus_opseq_init=ns.KrausOperatorSequence(ns.phase_flip(probability=0.2)),
	kraus_opseq_allgates=ns.KrausOperatorSequence(ns.depolarizing(probability=0.1)),
	kraus_opseq_qubits=ns.KrausOperatorApplierSequense(ns.KrausOperatorSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.add_noise_model(noise_model=noise_model)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=False)
bk = bknd.DMQdeb()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)


print('test 02 - DMQdeb, All KrausOperatorSequence')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.bit_flip(probability=0.1),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.phase_flip(probability=0.1))
ck.H([2])
noise_model = ns.NoiseModel(
	kraus_opseq_init=ns.phase_flip(probability=0.2),
	kraus_opseq_allgates=ns.depolarizing(probability=0.1),
	kraus_opseq_qubits=ns.KrausOperatorApplierSequense(ns.bit_flip(probability=0.3),[1]),
    )
ck.add_noise_model(noise_model=noise_model)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=False)
bk = bknd.DMQdeb()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)


print('test 03 - DMQeng, All KrausOperatorSequence')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.KrausOperatorSequence(ns.phase_flip(probability=0.1)))
ck.H([2])
noise_model = ns.NoiseModel(
	kraus_opseq_init=ns.KrausOperatorSequence(ns.phase_flip(probability=0.2)),
	kraus_opseq_allgates=ns.KrausOperatorSequence(ns.depolarizing(probability=0.1)),
	kraus_opseq_qubits=ns.KrausOperatorApplierSequense(ns.KrausOperatorSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.add_noise_model(noise_model=noise_model)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=False, verbose=False)
bk = bknd.DMQeng()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)


print('test 04 - DMQeng, All KrausOperatorSequence')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.bit_flip(probability=0.1),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.phase_flip(probability=0.1))
ck.H([2])
noise_model = ns.NoiseModel(
	kraus_opseq_init=ns.phase_flip(probability=0.2),
	kraus_opseq_allgates=ns.depolarizing(probability=0.1),
	kraus_opseq_qubits=ns.KrausOperatorApplierSequense(ns.bit_flip(probability=0.3),[1]),
    )
ck.add_noise_model(noise_model=noise_model)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=False, verbose=False)
bk = bknd.DMQeng()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)
