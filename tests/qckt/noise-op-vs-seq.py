#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns


print('test 01 - DMQdeb, All NoiseChannelSequence')
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
job = qckt.Job(ck,qtrace=True, verbose=False)
bk = bknd.DMQdeb()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)


print('test 02 - DMQdeb, All NoiseChannelSequence')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.bit_flip(probability=0.1),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).set_noise(ns.phase_flip(probability=0.1))
ck.H([2])
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.phase_flip(probability=0.2),
	noise_chan_allgates=ns.depolarizing(probability=0.1),
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.bit_flip(probability=0.3),[1]),
    )
ck.set_noise_profile(noise_profile=noise_profile)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=False)
bk = bknd.DMQdeb()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)


print('test 03 - DMQeng, All NoiseChannelSequence')
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
job = qckt.Job(ck,qtrace=False, verbose=False)
bk = bknd.DMQeng()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)


print('test 04 - DMQeng, All NoiseChannelSequence')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.bit_flip(probability=0.1),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).set_noise(ns.phase_flip(probability=0.1))
ck.H([2])
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.phase_flip(probability=0.2),
	noise_chan_allgates=ns.depolarizing(probability=0.1),
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.bit_flip(probability=0.3),[1]),
    )
ck.set_noise_profile(noise_profile=noise_profile)
ck.draw(show_noise=False)
ck.draw()
job = qckt.Job(ck,qtrace=False, verbose=False)
bk = bknd.DMQeng()
bk.runjob(job)
svec = job.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)
