#!/usr/bin/python3

import qcckt
import numpy as np
from fractions import gcd

nqbits = 8 # per the definition of f(x) below, must be >= 4
M = 2**(nqbits-2)

# setup the periodic function
fx = qcckt.QCkt(nqbits)
fx.Border()
fx.CX(2,0)
fx.CX(3,1)
fx.Border()
fx.draw()
print("Psst ... f(x) defined as having period of 4\n")

# Now loop to repeatedly find values of multiples of M/r by
# running the QC repeatedly and reading the outputs
idx = 0
vals = np.zeros(2)

# QFT(x) - F(x) - QFT(x) - Measure
ckt = qcckt.QCkt(nqbits)
ckt.QFT(list(range(nqbits-1,1,-1)))
fx = fx.realign(nqbits,nqbits, list(reversed(range(nqbits))))
ckt.append(fx)
ckt.QFT(list(range(nqbits-1,1,-1)))
ckt.M(list(range(nqbits-1,1,-1)),list(range(nqbits-1,1,-1)))
ckt.draw()

while idx < 2:
	# Restart the QC machine
	bk = qcckt.Backend()
	bk.run(ckt,qtrace=False)
	mbyrarr = bk.get_creg().value
	print("CREGISTER = ",bk.get_creg())
	# mbyrarr = q.qmeasure(list(range(nqbits-1,1,-1)))

	# convert to integer the measured values of the x register
	mbyr = 0
	for i in range(nqbits-2):
		sign = nqbits-2-1-i
		if mbyrarr[i] == 1:
			mbyr += 2**sign

	# Look for two distinc non-zero values
	print("a multiple of M/r = ",mbyr)
	if mbyr != 0:
		vals[idx] = mbyr
		if (vals[0] != vals[1]):
			idx += 1

	idx = 4

# find the GCD of the two values read to get M/r, and compute r, as M is known
mbyr = int(gcd(vals[0], vals[1]))
print("GCD of values of M/r = {:d}\n".format(mbyr))
print("But, M =", M)
r = int(M / mbyr)
print("Therefore, the period, r = ",r)
