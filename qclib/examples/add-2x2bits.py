#!/usr/bin/python3

print("""
PROBLEM STATEMENT:
Adds 2 2-bit numbers, result is 3-bits, and scratch register is 3-bits (to hold carry overs)
Total of 10 qubits, hence simulator runs quite slow - it took 4 minutes elapsed time on my old laptop.
The circuit used is --

        ci+1	----------o---o-----        --.--
        ci	------.---|---.-----        --|--
	              |   |   |               |
        bi	----.-|---.---|-----        --|--
        ai	--.-|-|---.---|-----        --|--
	          | | |       |               |
        si+1	--|-|-|-------|-----        --o--
        si	--o-o-o-----x-.-x---        -----

Need to copy the final carry-out bit into the highest order result bit, as shown.

""")

import qclib

q = qclib.qcsim(10,qtrace=True)

s = [0, 1, 2]	# sum bits - Result of addition
c = [3, 4, 5]	# carry bits, scratch pad register - Junk bits
b = [6, 7]	# input number B
a = [8, 9]	# input number A

H4 = q.qcombine_par("H4",[q.H(),q.H(),q.H(),q.H()])
q.qgate(H4,[a[0],a[1],b[0],b[1]])

# run the addition 
for i in range(2):
	print("Processing bit", i)
	q.qgate(q.C(),[a[i],s[i]])
	q.qgate(q.C(),[b[i],s[i]])
	q.qgate(q.C(),[c[i],s[i]])
	q.qgate(q.T(),[a[i],b[i],c[i+1]])
	q.qgate(q.X(),[s[i]])
	q.qgate(q.T(),[s[i],c[i],c[i+1]])
	q.qgate(q.X(),[s[i]])
q.qgate(q.C(),[c[2],s[2]])

# Clean up the junk bits
print("Cleaning up junk bits")
for i in reversed(range(2)):
	q.qgate(q.X(),[s[i]])
	q.qgate(q.T(),[s[i],c[i],c[i+1]])
	q.qgate(q.X(),[s[i]])
	q.qgate(q.T(),[a[i],b[i],c[i+1]])

q.qreport("Result")
