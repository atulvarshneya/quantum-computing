#!/usr/bin/python

import qclib
import numpy as np
from fractions import gcd

nqbits = 8 # must be >= 4
M = 2**(nqbits-2)
idx = 0
vals = np.zeros(2)
q = qclib.qcsim(nqbits)

# periodic function
op1 = q.qstretch(q.C(),[2,0])
op2 = q.qstretch(q.C(),[3,1])
f = q.qcombine_seq("F(x)",[op1,op2])
print "Psst ... f(x) defined as having period of 4"

while idx < 2:
	q.qreset()

	q.qgate(q.QFT(nqbits-2),range(nqbits-1,1,-1))
	q.qgate(f,list(reversed(range(nqbits))))
	# q.qmeasure([1,0])
	q.qgate(q.QFT(nqbits-2),range(nqbits-1,1,-1))
	mbyrarr = q.qmeasure(range(nqbits-1,1,-1))

	mbyr = 0
	for i in range(nqbits-2):
		sign = nqbits-2-1-i
		if mbyrarr[i] == 1:
			mbyr += 2**sign

	print "a multiple of M/r = ",mbyr
	if mbyr != 0:
		vals[idx] = mbyr
		if (vals[0] != vals[1]):
			idx += 1

mbyr = int(gcd(vals[0], vals[1]))
print "GCD of values of M/r =",mbyr
print "But, M =", M
r = int(M / mbyr)
print "Therefore, the period, r = ",r
