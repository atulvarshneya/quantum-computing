#!/usr/bin/env python

print("""
PROBLEM STATEMENT:
Adds 2 2-bit numbers, result is 3-bits, and scratch register is 2-bits holdch holds carry overs for bits 1 and 2,
there is no carry over value expected for bit 0, hence no qubit for that

Total of 9 qubits, hence simulator took just over 1 second elapsed time on my laptop.
The circuit blueprint used is --

        ci+1    ----------o---o-----        --.--
        ci      ------.---|---.-----        --|--
                      |   |   |               |
        bi      ----.-|---.---|-----        --|--
        ai      --.-|-|---.---|-----        --|--
                  | | |       |               |
        si+1    --|-|-|-------|-----        --o--
        si      --o-o-o-----x-.-x---        -----

Need to copy the final carry-out bit into the highest order result bit, as shown.

""")


import qckt
from QSystems import *
from Job import Job

nq = 9

s = [0, 1, 2]	# sum bits - Result of addition
c = [3, 4]	# carry bits, scratch pad register - Junk bits
b = [5, 6]	# input number B
a = [7, 8]	# input number A

addckt = qckt.QCkt(nq, nq)

addckt.H(a[0])
addckt.H(a[1])
addckt.H(b[0])
addckt.H(b[1])

# run the addition 
for i in range(2):
	# print("Processing bit", i)
	addckt.CX(a[i],s[i])
	addckt.CX(b[i],s[i])
	if i != 0:
		addckt.CX(c[i-1],s[i])
	addckt.CCX(a[i],b[i],c[i])
	if i != 0:
		addckt.X(s[i])
		addckt.CCX(s[i],c[i-1],c[i])
		addckt.X(s[i])
addckt.CX(c[1],s[2])

# Clean up the junk bits
for i in reversed(range(2)):
	if i != 0:
		addckt.X(s[i])
		addckt.CCX(s[i],c[i-1],c[i])
		addckt.X(s[i])
	addckt.CCX(a[i],b[i],c[i])
# addckt.M([0,1,2],[0,1,2])

addckt.draw()

job = Job(addckt,qtrace=True, verbose=False)
bk = Qdeb()
bk.runjob(job)
print()
print("READ OUT STATE VECTOR: ")
print(job.get_svec())
print("READ OUT CREGISTER: ", end="")
print( job.get_creg()[0])
print()
print('READ OUT RUNSTATS')
job.print_runstats()
