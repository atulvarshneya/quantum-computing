#!/usr/bin/python3

import qckt
import numpy as np
import random as rnd


def intro():
	print("""Grover's Algorithm.

Problem Statement:
Well known search algorithm by Lov Grover.

	      +----+     +------+     +----+    +------+    +----+
n-1	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
n-2	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
n-3	|0> --| Hn |-----|  Uf  |-----| Hn |----| UinvM|----| Hn |--- ... --(/)
	       ...         ...         ...        ...        ...
2	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
1	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
	      +----+     |      |     +----+    |      |    +----+
0	|-> -------------|      |---------------|      |-------------
                     +------+               +------+

	     \-Init-/  \------------------Iterate-------------------/  \-Measure-/
""")

#################################################################################
# Details @ https://en.wikipedia.org/wiki/Grover%27s_algorithm
#################################################################################

# intro()

nqbits = 5
marker = int(rnd.random() * (2**(nqbits-1)-1))
print(("Marker to search = {:0"+str(nqbits-1)+"b}").format(marker))

# 'needle' in the haytack = key
print("Building Uf circuit - phase inversion of the marker ...")
uf_ckt = qckt.QCkt(nqbits,name="Uf")
uf_ckt.Border()
x_list = []
for i in range(nqbits-1):
	if (marker & (0b1<<i)) == 0:
		x_list.append(i)
uf_ckt.X(x_list)
uf_ckt.CX(*[i for i in range(nqbits)])
uf_ckt.X(x_list)
uf_ckt.Border()
# uf_ckt.draw()

print("Buiding Amplifier circuit - phase inversion about the mean ...")
amp_ckt = qckt.QCkt(nqbits,name="Amplifier")
amp_ckt.H([i for i in range(nqbits-1)])
amp_ckt.X([i for i in range(nqbits-1)])
amp_ckt.CX(*[i for i in range(nqbits)])
amp_ckt.X([i for i in range(nqbits-1)])
amp_ckt.H([i for i in range(nqbits-1)])
# amp_ckt.draw()

print("Buiding Initializer circuit - uniform superposition ...")
init_ckt = qckt.QCkt(nqbits,name="Initialize")
init_ckt.H([i for i in range(nqbits-1)])
# setup the result qubit in |-> state for phase kickback
init_ckt.X(nqbits-1)
init_ckt.H(nqbits-1)
# init_ckt.draw()

fullckt = qckt.QCkt(nqbits)
fullckt = fullckt.append(init_ckt)
# fullckt.Probe("after initialization", probestates=[marker])
numitrs = int((np.pi/4.0) * (2.0**((nqbits-1.0)/2.0))) # optimal # iter, less or more dont work
print("number of Invert-Amplify iterations = ",numitrs)
for itr in range(numitrs):
	fullckt = fullckt.append(uf_ckt)
	fullckt = fullckt.append(amp_ckt)
	# fullckt.Probe("after iteration "+str(itr+1), probestates=[marker])
fullckt.M([i for i in range(nqbits-1)])
fullckt.draw()

print("Take from the following, best of 5 results...")
for m in range(5):  # Look for best of 5
	bk = qckt.Backend()
	bk.run(fullckt)

	res = bk.get_creg()
	print("Result = ",res)
