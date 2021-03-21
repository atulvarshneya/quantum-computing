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
qckt1.C(0,1)
qckt1.draw()

print("fragment of the final circuit-------------------")
qckt2 = qcckt.QCkt(4,name="ckt02")
qckt2.M([2,3])
qckt2.draw()

print("realigned subcircuit----------------------------")
qckt3 = qckt1.realignckt(4,4,[3,2])
qckt3.draw()

print("Overall circuit---------------------------------")
qckt4 = qckt3 + qckt2
qckt4.draw()

#test 02
print("================================================")
print("Test 02 ========================================")
print("Running circuits================================")
print("================================================")
qckt = qcckt.QCkt(2,2)
qckt.H(0)
qckt.C(0,1)
qckt.M([0,1])
qckt.draw()

bk = qcckt.Backend()
bk.run(qckt,qtrace=True)
bk.print_svec()

print(bk.get_creg())
