import qclib
import numpy as np
import random as rnd

theta = rnd.random() * 2 * np.pi
c = np.cos(theta)
s = np.sin(theta)
prep = np.matrix([[c,s]],dtype=complex)

q = qclib.qcsim(3,prepare=prep)
q.qreport()

# first put qbits 0 and 1 in bell state
q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])
# q.qreport("0 and 1 in bell state")
# qbit 1 is kept 'here' and qbit 0 is sent 'far away'; and we have the input qbit to be teleported, qbit 2, also 'here'.

# at 'here' we measure the qbit to be teleported and qbit 1 in bell basis.
mvals = q.qmeasure([2,1],basis=q.BELL_BASIS())
b0 = mvals[1]
b1 = mvals[0]

# now we send these classicla bits b0 and b1 to 'far away' and apply appropriate gates to recover the input bit's state in qbit 1
if b1 == 0 and b0 == 0:
	q.qgate(q.C(),[2,1])
	q.qgate(q.H(),[2])
elif b1 == 0 and b0 == 1:
	q.qgate(q.Z(),[0])

	# reset the state of 2 and 1, for clarity
	q.qgate(q.C(),[2,1])
	q.qgate(q.H(),[2])
	q.qgate(q.X(),[2])
elif b1 == 1 and b0 == 0:
	q.qgate(q.X(),[0])

	# reset the state of 2 and 1, for clarity
	q.qgate(q.C(),[2,1])
	q.qgate(q.H(),[2])
	q.qgate(q.X(),[1])
else:
	q.qgate(q.X(),[0])
	q.qgate(q.Z(),[0])

	# reset the state of 2 and 1, for clarity
	q.qgate(q.C(),[2,1])
	q.qgate(q.H(),[2])
	q.qgate(q.X(),[2])
	q.qgate(q.X(),[1])

q.qreport("Final state")
