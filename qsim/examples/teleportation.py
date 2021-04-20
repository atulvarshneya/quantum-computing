#!/usr/bin/python3

import qsim
import qgates as qgt
import numpy as np
import random as rnd

'''
This example shows an implementation of the teleportation protocol
The implementation done here demonstrates
	1. creating an initial state in qsim,
	2. measuring in a specific basis
'''

theta = rnd.random() * 2 * np.pi
c = np.cos(theta)
s = np.sin(theta)
# prepare the initial state with qbit-2 with the above computed random amplitude
msb = np.transpose(np.matrix([[c,s]],dtype=complex))
init = msb
for i in range(3-1):
	init = np.kron(init,np.transpose(np.matrix([[1,0]],dtype=complex)))


# now get started ...
q = qsim.QSimulator(3,initstate=init)
q.qreport(header="Initial State")

# first put qbits 0 and 1 in bell state
q.qgate(qgt.H(),[0])
q.qgate(qgt.C(),[0,1])
# q.qreport(header="0 and 1 in bell state")
# qbit 1 is kept 'here' and qbit 0 is sent 'far away'; and we have the input qbit to be teleported, qbit 2, also 'here'.

# at 'here' we measure the qbit to be teleported and qbit 1 in bell basis.
q.qgate(qgt.BELL_BASIS(),[2,1])
mvals = q.qmeasure([2,1])
q.qgate(q.qinverse(qgt.BELL_BASIS()),[2,1])
b0 = mvals[1]
b1 = mvals[0]

# now we send these classical bits b0 and b1 to 'far away' and apply appropriate gates to recover the input bit's state in qbit 1
if b1 == 0 and b0 == 0:
	q.qgate(qgt.C(),[2,1])
	q.qgate(qgt.H(),[2])
elif b1 == 0 and b0 == 1:
	q.qgate(qgt.Z(),[0])

	# reset the state of 2 and 1, for clarity
	q.qgate(qgt.C(),[2,1])
	q.qgate(qgt.H(),[2])
	q.qgate(qgt.X(),[2])
elif b1 == 1 and b0 == 0:
	q.qgate(qgt.X(),[0])

	# reset the state of 2 and 1, for clarity
	q.qgate(qgt.C(),[2,1])
	q.qgate(qgt.H(),[2])
	q.qgate(qgt.X(),[1])
else:
	q.qgate(qgt.X(),[0])
	q.qgate(qgt.Z(),[0])

	# reset the state of 2 and 1, for clarity
	q.qgate(qgt.C(),[2,1])
	q.qgate(qgt.H(),[2])
	q.qgate(qgt.X(),[2])
	q.qgate(qgt.X(),[1])

q.qreport(header="Final state")
