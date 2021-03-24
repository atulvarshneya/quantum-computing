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
qckt.CX(0,1)
qckt.QFT([0,1,2,3])
qckt.M([0,1])
qckt.draw()

bk = qcckt.Backend()
bk.run(qckt,qtrace=False)

svec = bk.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)
print("READ OUT STATE VECTOR (verbose): ")
svec.verbose(True)
print(svec)

# print cregister in proper MSB to LSB order
print("READ OUT CREGISTER: ",end="")
creg = bk.get_creg()
print(creg)
