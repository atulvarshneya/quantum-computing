#!/usr/bin/python3

import qcckt

# test 01
print("================================================")
print("Test 01 ========================================")
print("Composing circuits from subcircuits ============")
print("================================================")
print()
print("subcircuit--------------------------------------")
qckt1 = qcckt.QCkt(2,name="ckt01")
qckt1.H(0)
qckt1.CX(0,1)
qckt1.Border()
qckt1.draw()

print("subcircuit with QFT ----------------------------")
qckt2 = qcckt.QCkt(4,name="ckt02")
qckt2.QFT([2,0,3])
qckt2.X(2)
qckt2.Y(0)
qckt2.Z(3)
qckt2.Border()
qckt2.draw()

print("fragment of the final circuit-------------------")
qckt3 = qcckt.QCkt(4,name="ckt03")
qckt3.M([2,3])
qckt3.Border()
qckt3.draw()

print("realigned subcircuit----------------------------")
qckt1 = qckt1.realign(4,4,[3,2])
qckt1.draw()

print("realigned subcircuit----------------------------")
qckt2 = qckt2.realign(4,4,[1,3,0,2])
qckt2.draw()

print("Overall circuit---------------------------------")
qckt5 = (qckt1.append(qckt2)).append(qckt3)
qckt5.draw()

