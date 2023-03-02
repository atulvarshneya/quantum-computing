#!/usr/bin/env python

import qsim
import qgates as qgt
import numpy as np

q = qsim.QSimulator(3)

# put the qubit 2 in some randoom state
# this is the qubit that is to be teleported by Alice to Bob
print("\nThe qubit 2 is put in some random state, it will be teleported into qubit 0.")
q.qgate(qgt.RND(),[2], qtrace=True)

# get qubits 0 and 1 in the triplet state, |00> + |11>
# Alice and Bob have one of each of these entangled qubits
q.qgate(qgt.H(),[0])
q.qgate(qgt.C(),[0,1])

print( '''
cbit2  ============m=======.==
                   |       |
cbit1  ========m===|===.===|==
               |   |   |   |
qubit2 -.-[H]-(/)------|---|--
        |              |   |
qubit1 -o---------(/)--|---|--
                       |   |
qubit0 ---------------[X]-[Z]-- qubit 2 teleported into qubit 0

''')

print("Starting the teleportation protocol...")
q.qgate(qgt.C(),[2,1])
q.qgate(qgt.H(),[2])
q.qmeasure([1])
q.qmeasure([2])

q.qgate(qgt.X(),[0], ifcbits=[1])
q.qgate(qgt.Z(),[0], ifcbits=[2])

q.qreport()
print("qubit 2 teleported into qubit 0.")
