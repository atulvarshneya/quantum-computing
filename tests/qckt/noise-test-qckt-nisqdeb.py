#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns
import numpy as np


# print the list of canned kraus channels
noise_channels = list(ns.noise_operator_list().keys())
noise_channels.sort()
print(noise_channels)
print()

# test 01 - without any noise model
print('test 01 - without any noise model')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.CX(0,1)
ck.X([2])
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.NISQdeb()
bk.runjob(job)

# test 02 - direct call to qnoise
print('test 02 - direct call to qnoise')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2])
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.NISQdeb()
bk.runjob(job)

# test 03 - adding noise applied to a gate invokation
print('test 03 - adding noise applied to a gate invokation')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).add_noise(ns.KrausOperatorSequence(ns.phase_flip(probability=0.1)))
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.NISQdeb()
bk.runjob(job)

# test 04 - adding noise at init, applied to specifc qubits, all gates
print('test 04 - adding noise at init, applied to specifc qubits, all gates')
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
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.NISQdeb()
bk.runjob(job)

# test 05 - a blanket test for all noise operators applied to all gates, using their default arguments
for nchanid in noise_channels:
    if ns.noise_operator_lookup(nchanid)().nqubits != 1:
        # print(f'skipped {nchanid}')
        continue
    print(f'test 05 - Blanket test - {nchanid}')
    krfn = ns.noise_operator_lookup(nchanid)
    ck = qckt.QCkt(3,3)
    ck.X([0])
    ck.NOISE(kraus_ops=ns.KrausOperatorSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
    ck.CX(0,1)
    ck.X([2]).add_noise(ns.KrausOperatorSequence(ns.phase_flip(probability=0.1)))
    ck.H([2])
    noise_model = ns.NoiseModel(
        kraus_opseq_allgates=ns.KrausOperatorSequence(krfn()),
        kraus_opseq_init=None
        )
    ck.add_noise_model(noise_model=noise_model)
    ck.draw(show_noise=False)
    ck.draw()
    job = qckt.Job(ck,qtrace=True, verbose=True)
    bk = bknd.NISQdeb()
    bk.runjob(job)

# test06 - 2-qubit dummy kraus operator
print(f'test06 - 2-qubit dummy kraus operator')
ck = qckt.QCkt(3,3)
ck.H([0])
ck.CX(0,1).add_noise(ns.dummy_2qubit_kop(probability=0.5))
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.NISQdeb()
bk.runjob(job)

# test07 - custom gates with noise_to_each(), add_noise()
print('test07 - custom gates with noise_to_each()')
ck = qckt.QCkt(3,3)
ck.custom_gate('myX', np.matrix([[0.0,1.0],[1.0,0.0]],dtype=complex))
ck.custom_gate('myCX', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,0.0,1.0],[0.0,0.0,1.0,0.0]],dtype=complex))
ck.myX.noise_to_each(ns.bit_flip(0.2))
ck.myX(0)
ck.H(0)
ck.CX(0,1)
ck.myX(2)
ck.myX(0).add_noise(ns.phase_flip(0.3))
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.NISQdeb()
bk.runjob(job)


# test0x - list noise channel/operator signatures
noise_chans_list = ns.noise_operator_list()
for nchanid in noise_chans_list.keys():
	print(f'{nchanid:30s}  {noise_chans_list[nchanid]}')