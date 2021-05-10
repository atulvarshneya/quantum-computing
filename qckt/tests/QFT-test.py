#!/usr/bin/python3

import qckt
import numpy as np
from QSystems import *

nqbits = 8 # per the definition of f(x) below, must be >= 4
M = 2**(nqbits-2)
cktf = qckt.QCkt(nqbits)
cktf.CX(2,0)
cktf.CX(3,1)
print("Psst ... f(x) defined as having period of 4\n")

ckt = qckt.QCkt(nqbits)
ckt.X(0)
ckt.QFT(*(range(nqbits-1,1,-1)))
ckt = ckt.append(cktf)
ckt.QFT(*(range(nqbits-1,1,-1)))
ckt.draw()

bk = Backend()
bk.run(ckt,qtrace=False)

svec = bk.get_svec()
print("READ OUT STATE VECTOR: ")
print(svec)

print("READ OUT CREGISTER: ",end="")
creg = bk.get_creg()
print(creg)
