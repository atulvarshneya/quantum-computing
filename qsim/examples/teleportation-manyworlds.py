#!/usr/bin/env python

import qsim
import qgates as qgt
import numpy as np
import random as rnd

'''
This example shows an implementation of the teleportation protocol 
with qubits 5 and 4 representing the state of the worlds. 
Qubit 5 represents 'what I observed qubit 1 to be' and qubit 4 
represents 'what I observed qubit 2 to be'. 
So, Qubits 5 and 4 identify the 4 possible branches in the many-worlds.
'''

'''
This implementation follows slightly different version of the algorithm
than the other telepotation example in this folder.
'''

NQUBITS=6
# Note: qubit 3 is not used, it is just a 'space' between the 
# qubits involved in the algorithm and the bits identifying 
# the worlds.

# Prepare a qubit in some random state
theta = rnd.random() * 2 * np.pi
c = np.cos(theta)
s = np.sin(theta)
# prepare the initial state with the above qubit as qbit-2
tbit = np.transpose(np.matrix([[c,s]],dtype=complex))
initstate = np.transpose(np.matrix([[1,0]],dtype=complex))
for i in range(NQUBITS-1):
	if i == 2:
		initstate = np.kron(initstate,tbit)
	else:
		initstate = np.kron(initstate,np.transpose(np.matrix([[1,0]],dtype=complex)))

# now get started ...
q = qsim.QSimulator(NQUBITS,initstate=initstate)
q.qreport(header="Initial State")

# first put qbits 0 and 1 in bell state
q.qgate(qgt.H(),[0])
q.qgate(qgt.C(),[0,1])
q.qreport(header="0 and 1 in bell state")
# qbit 1 is kept 'here' and qbit 0 is sent 'far away'; and we have 
# the input qbit to be teleported, qbit 2, also 'here'.

# at 'here' we CNOT qbit 2 (control qubit) and qbit 1 
q.qgate(qgt.C(), [2,1])
# at 'here' perform H on qubit 2 (the qubit to be teleported)
q.qgate(qgt.H(),[2])
q.qreport(header="C(2,1), H(2)")

# Now "measure" qubits 1 and 2
# OK, we do this measurement as if we are combination of qubits 5 and 4.
# So, qubit 5 measures (gets entangled with) qubits 1 and represents 
# the state 'what I observed  1 as' and then qubit 4 entangles with 
# qubit 2 and represents the state 'what I observed 2 as'.
# The worlds splits into 4 branches as following --
#                ==
#               /
#         == m(2)
#        /      \
#       /        ==
# === m(1)
#       \        ==
#        \      /
#         == m(2)
#               \
#                ==
q.qgate(qgt.C(), [1,5])
q.qgate(qgt.C(), [2,4])
q.qreport(header="q5 measured q1, and q4 measured q2")

# OK, now we pick any one branch of the 4 branched worlds we 
# concurrently live in. We do that by a trick in the simulator -
# we perform a measurement on the observer qubits 5 and 4.
q.qmeasure([5,4])
q.qreport(header="Picking one branch of the many-worlds")

# Now we continue with the algorith. We measure the qubits 2 1nd 1 
# and pass that classical information to 'far away' location where 
# qubit 0 resides. And based on that classical information we 
# conditionally apply X and Z gates to complete the teleportation.
mvals = q.qmeasure([2,1])
mq2 = mvals[0]
mq1 = mvals[1]
if mq1 == 1:
	q.qgate(qgt.X(), [0])
if mq2 == 1:
	q.qgate(qgt.Z(), [0])

q.qreport(header="Final state")

