import qclib
import numpy as np
import random as rnd

theta = rnd.random() * 2 * np.pi
c = np.cos(theta)
s = np.sin(theta)
prep = np.matrix([[c,s]],dtype=complex)

q = qclib.qcsim(4,prepare=prep)
q.qreport()

# first put qbits 0 and 1 in bell state
q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])
q.qreport("0 and 1 in bell state")
# qbit 0 is kept 'here' and qbit 1 is sent 'far away'; and we have the input qbit to be teleported, qbit 3, also 'here'.

# at 'here' we measure the qbit to be teleported and qbit 0 in bell basis.

# now we send these classicla bits b0 and b1 to 'far away' and apply appropriate gates to recover the input bit's state in qbit 1
