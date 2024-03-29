#!/usr/bin/env python

import qckt
import qckt.noisemodel as ns

# test 01
print("================================================")
print("Composing circuits from subcircuits ============")
print("================================================")
print()
print("subcircuit--------------------------------------")
qckt1 = qckt.QCkt(2,name="ckt01")
qckt1.H(0)
qckt1.CX(0,1)
qckt1.Border()
qckt1.draw()
qckt1.list()

print("subcircuit with QFT ----------------------------")
qckt2 = qckt.QCkt(4,name="ckt02")
qckt2.QFT(2,0,3)
qckt2.X(2)
qckt2.Y(0)
qckt2.Z(3)
qckt2.Border()
qckt2.draw()
qckt2.list()

print("fragment of the final circuit-------------------")
qckt3 = qckt.QCkt(4,4,name="ckt03")
qckt3.M([2,3])
qckt3.Border()
qckt3.draw()
qckt3.list()

print("realigned subcircuit----------------------------")
qckt1 = qckt1.realign(4,4,[3,2])
qckt1.draw()
qckt1.list()

print("realigned subcircuit----------------------------")
qckt2 = qckt2.realign(4,4,[1,3,0,2])
qckt2.draw()
qckt2.list()

print("Overall circuit---------------------------------")
qckt5 = (qckt1.append(qckt2)).append(qckt3)
qckt5.draw()
qckt5.list()

#### RND, P, CP, SWAP and UROTk gates draw and list
print()
print("================================================")
print("RND, P, UROTk gates draw and list test===========")
print("================================================")

ck = qckt.QCkt(4)
ck.RND(0)
ck.P(3.14/4,1)
ck.CP(3.14/8,0,3)
ck.UROTk(3,2)
ck.CROTk(3,2,0)
ck.SWAP(1,3)
ck.CCX(0,2,3)
ck.CCX(2,3,0)
ck.draw()
ck.list()
ck = ck.realign(6,6,[3,0,2,1])
ck.draw()
ck.list()

#### multiple qbits inputs for single qubit gates draw and list
print()
print("================================================================")
print("multiple inputs X, Y, Z, H, P, UROTk gates draw and list test===")
print("================================================================")

ck = qckt.QCkt(8)
ck.X([0,1,2,3])
ck.Y([1,2,3,4])
ck.Z([2,3,4,5])
ck.H([3,4,5,6])
ck.P(3.14/2,[4,5,6,7])
ck.UROTk(2,[2,3,4,5,6,7])
ck.list()
ck.draw()


#### sniff test for drawing and listing noise elements
print()
print("================================================================")
print("sniff test for drawing and listing noise elements===============")
print("================================================================")

ck = qckt.QCkt(2,2,name='Test circuit for draw, list')
ck.H(0)
ck.CX(0,1).ifcbit(1,1)
ck.P(3.14,[0,1])
ck.UROTk(2,0)
ck.NOISE(ns.bit_flip(0.5),[0,1])
ck.M([1,0],[1,0])
ck.Probe()

ck.set_noise_profile(noise_profile=ns.NoiseProfile(
    noise_chan_init=ns.bit_flip(probability=0.1),
    noise_chan_allgates=ns.depolarizing(probability=0.2),
    noise_chan_qubits=ns.NoiseChannelApplierSequense(noise_chan=ns.amplitude_damping(gamma=0.3),qubit_list=[1]),
    noise_chan_allsteps=ns.NoiseChannelApplierSequense(noise_chan=ns.phase_damping(gamma=0.4),qubit_list=[1]),
    )
)
ck.list(show_noise=True)
print()
ck.draw(show_noise=True)
print()
ck.list(show_noise=False)
print()
ck.draw(show_noise=False)
print()
