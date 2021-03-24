#!/usr/bin/python3

import qcckt
import numpy as np
from fractions import gcd
import math

nqbits = 8 # per the definition of f(x) below, must be >= 4
M = 2**(nqbits-2)

# setup the periodic function
fx = qcckt.QCkt(nqbits)
fx.Border()
fx.CX(2,0)
fx.CX(3,1)
fx.Border()
print("Psst ... f(x) defined as having period of 4\n")

# QFT(x) - F(x) - QFT(x) - Measure
ckt = qcckt.QCkt(nqbits)
ckt.QFT(list(range(nqbits-1,1,-1)))
ckt.append(fx)
# actually you would expect to measure output of fx now
# ckt.M([0,1])
# but due to principle of defered measurement, it is not necessary
ckt.QFT(list(range(nqbits-1,1,-1)))
ckt.M(list(range(nqbits-1,1,-1)))
ckt.draw()

# Now loop to repeatedly find values of multiples of M/r by
# running the circuit repeatedly and reading the outputs
idx = 0
vals = [0,0]
while idx < 2:
	# run the circuit
	bk = qcckt.Backend()
	bk.run(ckt,qtrace=False)
	mbyrarr = bk.get_creg().value
	print("CREGISTER = ",bk.get_creg())
	# mbyrarr = q.qmeasure(list(range(nqbits-1,1,-1)))

	# convert to integer the measured values of the x register
	# remember the Cregister holds *all* classical bits, not just the ones measured
	mbyr = 0
	for i in range(2,nqbits):
		pow_of_2 = i-2
		if mbyrarr[i] == 1:
			mbyr += 2**pow_of_2

	# Look for two distinc non-zero values
	print("a multiple of M/r = ",mbyr)
	if mbyr != 0:
		vals[idx] = int(mbyr)
		if (vals[0] != vals[1]):
			idx += 1

# find the GCD of the two values read to get M/r, and compute r, as M is known
mbyr = int(math.gcd(vals[0], vals[1]))
print("GCD of values of M/r = {:d}\n".format(mbyr))
print("But, M =", M)
r = int(M / mbyr)
print("Therefore, the period, r = ",r)
