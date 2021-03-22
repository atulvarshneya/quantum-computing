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


import qcckt

nq = 10

s = [0, 1, 2]	# sum bits - Result of addition
c = [3, 4, 5]	# carry bits, scratch pad register - Junk bits
b = [6, 7]	# input number B
a = [8, 9]	# input number A

addckt = qcckt.QCkt(nq, nq)

addckt.H(a[0])
addckt.H(a[1])
addckt.H(b[0])
addckt.H(b[1])

# run the addition 
for i in range(2):
	# print("Processing bit", i)
	addckt.C(a[i],s[i])
	# q.qgate(q.C(),[a[i],s[i]])
	addckt.C(b[i],s[i])
	# q.qgate(q.C(),[b[i],s[i]])
	addckt.C(c[i],s[i])
	# q.qgate(q.C(),[c[i],s[i]])
	addckt.T(a[i],b[i],c[i+1])
	# q.qgate(q.T(),[a[i],b[i],c[i+1]])
	addckt.X(s[i])
	# q.qgate(q.X(),[s[i]])
	addckt.T(s[i],c[i],c[i+1])
	# q.qgate(q.T(),[s[i],c[i],c[i+1]])
	addckt.X(s[i])
	# q.qgate(q.X(),[s[i]])
addckt.C(c[2],s[2])
# q.qgate(q.C(),[c[2],s[2]])

# Clean up the junk bits
for i in reversed(range(2)):
	addckt.X(s[i])
	# q.qgate(q.X(),[s[i]])
	addckt.T(s[i],c[i],c[i+1])
	# q.qgate(q.T(),[s[i],c[i],c[i+1]])
	addckt.X(s[i])
	# q.qgate(q.X(),[s[i]])
	addckt.T(a[i],b[i],c[i+1])
	# q.qgate(q.T(),[a[i],b[i],c[i+1]])
# addckt.M([0,1,2],[0,1,2])

addckt.draw()

bk = qcckt.Backend()
bk.run(addckt,qtrace=True)
print()
print("READ OUT STATE VECTOR: ")
print(bk.get_svec())
print("READ OUT CREGISTER: ", end="")
print( bk.get_creg())
