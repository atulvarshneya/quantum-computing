#!/usr/bin/python3

import qckt

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
qckt2.QFT([2,0,3])
qckt2.X(2)
qckt2.Y(0)
qckt2.Z(3)
qckt2.Border()
qckt2.draw()
qckt2.list()

print("fragment of the final circuit-------------------")
qckt3 = qckt.QCkt(4,name="ckt03")
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

#### RND, ROT and Rk gates draw and list
print()
print("================================================")
print("RND, ROT, Rk gates draw and list test===========")
print("================================================")

ck = qckt.QCkt(4)
ck.RND(0)
ck.ROT(3.14/4,1)
ck.Rk(3,2)
ck.SWAP(1,3)
ck.draw()
ck.list()
