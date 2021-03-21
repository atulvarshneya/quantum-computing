#!/usr/bin/python3

'''
This is a program to simulate an experiment similar to two-slit experiment.

        |             |
        | D           |
       0              X
        |             |
        |             |
       1              Y
        |             |
        |             |

The two slits are marked as 0 and 1, and the observations are made on the screen
at locations X and Y. There is also a detector D right next to the slit 0, which
on detecting the electron at 0 gets entangled with it.

We formulate the states as:

The electron passes the two slits as in states |0> and |1>,
the lables of the kets represent the slit where the
electron passes through. If the electron passes through only
one slit (say, the other one is closed) its state will be
either |0> or |1>. If both the slits are open, the electron
would be in a superposition of both the states (|0> + |1>)/sqrt(2)

The unitary transform to map the states from |0> or |1> to X (|0>),
and Y (|1>) is taken to be Hadamard - this unitary transform will
cause an interference pattern. So, when starting in above mentioned
superposition, the observation at the screen will be
	1/sqrt(2)(1/sqrt(2)(|0> + |1> + |0> - |1>))
	= 1/2 (2 * |0>)
	= |0>

Now let us consider the detector D detects (gets entangled with)
the electron. The state of the detector is |0> if it finds the
electron has passed through slit 0, or |1> otherwise (the electron
has passed through slit 1). Hence the combined state of the electron
and the detector will be (|00> + |11>)/sqrt(2), if the measurement
is 'strong', implying that they are fully entangled. In reality the
degree of entanglement can be partial, in that case the state will be
	a|00> + b|01> + c|10> + d|11>

The program below computes the probability of detecting the electron
at X vs Y with different degrees of entanglement with the detector D

        |             |
        | D           |
       0              X
        |             |
        |             |
       1              Y
        |             |
        |             |

  initial  ---[H0]---(/)
  state             measure

The idea is that if the entanglement is absent (no measurement),
the interference pattern will be absolutely clear; as entanglement
increases (definiteness in measurement increases), the interference
pattern will weaken. If the entangelment is full (definite measurement),
the interference will be gone.

The program creates an initial state as it would be right after the electron
has passed the detector D. It creates this state with different degrees of
entanglement, and then after applying the unitary transform (Hadamard), it 
does the measurement of the location of the electron (qubit 0).

'''

import numpy as np
import qclib

for e in range(11):
	# 1. one-after-another create states of different entangelment with D
	istarr = [1.0-e/10.0,e/10.0,e/10.0,1.0-e/10.0]
	norm = 0.0
	for s in istarr:
		norm += s*s
	norm = np.sqrt(norm)
	istarr = istarr/norm
	ist = np.transpose(np.matrix(istarr,dtype=complex))

	# 2. Initialize the QSIM with that as the initial state
	q = qclib.qcsim(2,initstate=ist,validation=True)

	# 3. now run the test 'sample' number of times to get statistics
	samples = 1000
	dist = [0]*2
	for i in range(samples):
		q.qreset()
		q.qgate(q.H(),[0])
		m = q.qmeasure([0])
		v = m[0]
		dist[v] += 1

	# 4. Pretty print the results
	str_dist = ""
	for i in range(2):
		str_dist += "	|"+str(i)+"> "+str(np.round(100.0*float(dist[i])/float(samples),decimals=2))+"%"
	str_is = "[ "
	for v in istarr: str_is += "{:0.2f} ".format(v)
	str_is += "]"
	print(str_is, str_dist)
