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


import qsim
import qgates as qgt
import qgatesUtils as qgu

q = qsim.QSimulator(9,qtrace=False)

s = [0, 1, 2]	# sum bits - Result of addition
c = [3, 4]	# carry bits, scratch pad register - Junk bits
b = [5, 6]	# input number B
a = [7, 8]	# input number A

H4 = qgu.qcombine_par("H4",[qgt.H(),qgt.H(),qgt.H(),qgt.H()])
q.qgate(H4,[a[0],a[1],b[0],b[1]])

# run the addition 
for i in range(2):
	print("Processing bit", i)
	q.qgate(qgt.C(),[a[i],s[i]])
	q.qgate(qgt.C(),[b[i],s[i]])
	if i != 0:
		q.qgate(qgt.C(),[c[i-1],s[i]])
	q.qgate(qgt.T(),[a[i],b[i],c[i]])
	if i != 0:
		q.qgate(qgt.X(),[s[i]])
		q.qgate(qgt.T(),[s[i],c[i-1],c[i]])
		q.qgate(qgt.X(),[s[i]])
q.qgate(qgt.C(),[c[1],s[2]])

# Clean up the junk bits
print("Cleaning up junk bits")
for i in reversed(range(2)):
	if i != 0:
		q.qgate(qgt.X(),[s[i]])
		q.qgate(qgt.T(),[s[i],c[i-1],c[i]])
		q.qgate(qgt.X(),[s[i]])
	q.qgate(qgt.T(),[a[i],b[i],c[i]])

q.qreport("Result")
