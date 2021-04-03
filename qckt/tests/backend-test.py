#!/usr/bin/python3

import qckt

#test 02
nq = 6
qc = qckt.QCkt(nq,nq)
qc.H(0)
qc.CX(0,1)
qc.QFT(0,1,2,3)
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

bk = qckt.Backend()
bk.run(ck,qtrace=True)

svec = bk.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)
print("READ OUT STATE VECTOR (verbose): ")
svec.verbose(True)
print(svec)

