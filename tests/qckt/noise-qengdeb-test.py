#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns

# added noise profile, but using Qdeb
print('added noise profile, but using Qdeb')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.NoiseChannelSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).set_noise(ns.NoiseChannelSequence(ns.phase_flip(probability=0.1)))
# ck.H([2])
ck.M([2,1,0])
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.NoiseChannelSequence(ns.phase_flip(probability=0.2)),
	noise_chan_allgates=ns.NoiseChannelSequence(ns.depolarizing(probability=0.1)),
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.NoiseChannelSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.set_noise_profile(noise_profile=noise_profile)
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

# added noise profile, but using Qeng
print('added noise profile, but using Qeng')
ck = qckt.QCkt(3,3)
ck.X([0])
ck.NOISE(noise_chan=ns.NoiseChannelSequence(ns.bit_flip(probability=0.1)),qbit=[0,1,2])
ck.CX(0,1)
ck.X([2]).set_noise(ns.NoiseChannelSequence(ns.phase_flip(probability=0.1)))
# ck.H([2])
ck.M([2,1,0])
noise_profile = ns.NoiseProfile(
	noise_chan_init=ns.NoiseChannelSequence(ns.phase_flip(probability=0.2)),
	noise_chan_allgates=ns.NoiseChannelSequence(ns.depolarizing(probability=0.1)),
	noise_chan_qubits=ns.NoiseChannelApplierSequense(ns.NoiseChannelSequence(ns.bit_flip(probability=0.3)),[1]),
    )
ck.set_noise_profile(noise_profile=noise_profile)
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
