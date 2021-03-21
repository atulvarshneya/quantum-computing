#!/usr/bin/python3

import qcckt

#test 02
print("================================================")
print("Test 02 ========================================")
print("Running circuits================================")
print("================================================")
nq = 4
qckt = qcckt.QCkt(nq,nq)
qckt.H(0)
qckt.C(0,1)
qckt.M([0,1])
qckt.draw()

bk = qcckt.Backend()
bk.run(qckt,qtrace=True)

print()
print("READ OUT STATE VECTOR: ")
bk.print_svec()
# print cregister in proper MSB to LSB order
print()
print("READ OUT CREGISTER: ",end="")
creg = bk.get_creg()
for i in reversed(range(nq)):
	print("{0:01b}".format(creg[i]),end="")
print()
