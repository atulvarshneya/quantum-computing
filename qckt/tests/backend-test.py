#!/usr/bin/python3

import qckt

#test 02
print("================================================")
print("Test 02 ========================================")
print("Running circuits================================")
print("================================================")
nq = 6
qc = qckt.QCkt(nq,nq)
qc.H(0)
qc.CX(0,1)
qc.QFT([0,1,2,3])
qc.X(4)
qc.Y(5)
qc.M([4,5])
qc.draw()

bk = qckt.Backend()
bk.run(qc,qtrace=False)

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
