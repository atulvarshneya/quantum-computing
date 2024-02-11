#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns
import numpy as np


# print the list of canned noise channels
noise_channels = list(ns.noise_channel_list().keys())
noise_channels.sort()
print(noise_channels)
print()

# test 01 - without any noise profile
print('test 01 - without any noise profile')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.CX(0,1)
ck.X([2])
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test 02 - direct call to qnoise
print('test 02 - direct call to qnoise')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.NoiseChannelSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2])
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test 03 - adding noise applied to a gate invokation
print('test 03 - adding noise applied to a gate invokation')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.NoiseChannelSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
# ck.X([2]).set_noise(ns.NoiseChannelSequence(ns.phase_flip(probability=0.1)))
ck.X([2]).set_noise(ns.phase_flip(probability=0.1))
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test 04 - adding noise at init, applied to specifc qubits, all gates
print('test 04 - adding noise at init, applied to specifc qubits, all gates')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.NoiseChannelSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).set_noise(ns.NoiseChannelSequence(ns.phase_flip(probability=0.1)))
ck.H([2])
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.NoiseChannelSequence(ns.phase_flip(probability=0.2)),
	noise_chan_allgates=ns.NoiseChannelSequence(ns.depolarizing(probability=0.1)),
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.NoiseChannelSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.set_noise_profile(noise_profile=noise_profile)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test 05 - a blanket test for all noise operators applied to all gates, using their default arguments
for nchanid in noise_channels:
    if ns.noise_channel_lookup(nchanid)().nqubits != 1:
        # print(f'skipped {nchanid}')
        continue
    print(f'test 05 - Blanket test - {nchanid}')
    krfn = ns.noise_channel_lookup(nchanid)
    ck = qckt.QCkt(3,3)
    ck.X([0])
    ck.NOISE(noise_chan=ns.NoiseChannelSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
    ck.CX(0,1)
    ck.X([2]).set_noise(ns.NoiseChannelSequence(ns.phase_flip(probability=0.1)))
    ck.H([2])
    noise_profile = ns.NoiseProfile(
        noise_chan_allgates=ns.NoiseChannelSequence(krfn()),
        noise_chan_init=None
        )
    ck.set_noise_profile(noise_profile=noise_profile)
    ck.draw(show_noise=False)
    ck.draw()
    job = qckt.Job(ck,qtrace=True, verbose=True)
    bk = bknd.DMQdeb()
    bk.runjob(job)

# test06 - 2-qubit dummy noise channel
print(f'test06 - 2-qubit dummy noise channel')
ck = qckt.QCkt(3,3)
ck.H([0])
ck.CX(0,1).set_noise(ns.dummy_2qubit_chan(probability=0.5))
ck.H([2])
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test07 - user defined gates with set_noise_on_all(), set_noise()
print('test07 - custom gates with set_noise_on_all()')
qckt.define_gate('myX', np.matrix([[0.0,1.0],[1.0,0.0]],dtype=complex))
qckt.define_gate('myCX', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,0.0,1.0],[0.0,0.0,1.0,0.0]],dtype=complex))
ck = qckt.QCkt(3,3)
ck.myX.set_noise_on_all(ns.bit_flip(0.2))
ck.myX(0)
ck.H(0)
ck.CX(0,1)
ck.myX(2)
ck.myX(0).set_noise(ns.phase_flip(0.3))
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test08 - catch error on multi-quibit NoiseChannel on mismatched qubit gate
print('test08 - catch error on multi-quibit NoiseChannel on mismatched qubit gate')
ck = qckt.QCkt(3,3)
try:
    ck.H(0).set_noise(ns.two_qubit_dephasing(0.2))
except Exception as e:
    print(e)
ck.H.set_noise_on_all(ns.two_qubit_dephasing(0.3))
try:
    ck.draw()
except Exception as e:
    print(e)
try:
    job = qckt.Job(ck,qtrace=True, verbose=True)
    bk = bknd.DMQdeb()
    bk.runjob(job)
except Exception as e:
    print(e)
print()

# test0x - list noise channel/operator signatures
noise_chans_list = ns.noise_channel_list()
for nchanid in noise_chans_list.keys():
	print(f'{nchanid:30s}  {noise_chans_list[nchanid]}')
