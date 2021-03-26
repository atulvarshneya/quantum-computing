#!/usr/bin/python3

import qsim
import numpy as np

q = qsim.QSimulator(3)

# put the qubit 2 in some randoom state
# this is the qubit that is to be teleported by Alice to Bob
print("\nThe qubit 2 is put in some random state, it will be teleported into qubit 0.")
q.qgate(q.RND(),[2], qtrace=True)

# get qubits 0 and 1 in the triplet state, |00> + |11>
# Alice and Bob have one of each of these entangled qubits
q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])

'''
2 -.-[H]-(/)------.--
   |              |
1 -o-----(/)--.---|--
              |   |
0 -----------[X]-[Z]-- qubit 2 teleported into qubit 0

Clearly, while much simpler to understand, this is not a practical way 
of doing it, as the controlled X and controlled Z gates will need to 
span the physical distance betwee where Alice and Bob are.

'''

print("\nStarting the teleportation protocol...")
q.qgate(q.C(),[2,1])
q.qgate(q.H(),[2])
qbit1 = q.qmeasure([1])[0]
qbit2 = q.qmeasure([2])[0]

q.qgate(q.CTL(q.X()),[1,0])
q.qgate(q.CTL(q.Z()),[2,0])

# Aesthetic cleanup of qbits 2 and 1
if qbit1 == 1:
	q.qgate(q.X(),[1])
if qbit2 == 1:
	q.qgate(q.X(),[2])

q.qreport()
print("qubit 2 teleported into qubit 0.")
