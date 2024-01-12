#!/usr/bin/env python

import qckt
import qckt.noisemodel as ns
import qckt.backend as bknd

print('01 adding noise at init, applied to specifc qubits, all gates, all steps')
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.NoiseChannelSequence(ns.phase_flip(probability=0.2)),
	noise_chan_allgates=ns.NoiseChannelSequence(ns.depolarizing(probability=0.1)),
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.NoiseChannelSequence(ns.bit_flip(probability=0.3)),[1]),
    noise_chan_allsteps=ns.NoiseChannelApplierSequense(noise_chan=ns.amplitude_damping(gamma=0.1),qubit_list=[0,1]),
)

ck = qckt.QCkt(2,2)
ck.H(0)
ck.CX(0,1)

ck.set_noise_profile(noise_profile=noise_profile)
ck.draw()

job = qckt.Job(circuit=ck,qtrace=True)
bk = bknd.DMQdeb()
bk.runjob(job=job)


print('02 noise at init')
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.NoiseChannelSequence(ns.phase_flip(probability=0.2)),
)

ck = qckt.QCkt(2,2)
ck.H(0)
ck.CX(0,1)

ck.set_noise_profile(noise_profile=noise_profile)
ck.draw()

job = qckt.Job(circuit=ck,qtrace=True)
bk = bknd.DMQdeb()
bk.runjob(job=job)


print('03 noise applied to specifc qubits')
noise_profile = ns.NoiseProfile(
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.NoiseChannelSequence(ns.bit_flip(probability=0.3)),[1]),
)

ck = qckt.QCkt(2,2)
ck.H(0)
ck.CX(0,1)

ck.set_noise_profile(noise_profile=noise_profile)
ck.draw()

job = qckt.Job(circuit=ck,qtrace=True)
bk = bknd.DMQdeb()
bk.runjob(job=job)



print('04 noise on all gates')
noise_profile = ns.NoiseProfile(
	noise_chan_allgates=ns.NoiseChannelSequence(ns.depolarizing(probability=0.1)),
)

ck = qckt.QCkt(2,2)
ck.H(0)
ck.CX(0,1)

ck.set_noise_profile(noise_profile=noise_profile)
ck.draw()

job = qckt.Job(circuit=ck,qtrace=True)
bk = bknd.DMQdeb()
bk.runjob(job=job)



print('05 noise at all steps')
noise_profile = ns.NoiseProfile(
    noise_chan_allsteps=ns.NoiseChannelApplierSequense(noise_chan=ns.bit_flip(probability=0.1),qubit_list=[0,1]),
)

ck = qckt.QCkt(2,2)
ck.H(0)
ck.CX(0,1)

ck.set_noise_profile(noise_profile=noise_profile)
ck.draw()

job = qckt.Job(circuit=ck,qtrace=True)
bk = bknd.DMQdeb()
bk.runjob(job=job)