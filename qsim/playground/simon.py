#!/usr/bin/python3

'''
 x  f(x)
000 101
001 010
010 000
011 110
100 000
101 110
110 101
111 010
'''

import qsim
import numpy as np

nqbits = 6

initstate = np.transpose(np.matrix([None]*(2**nqbits),dtype=complex))
for i in range(2**nqbits):
	initstate[i] = 0.0+0.0j
amp = np.sqrt(1.0/(2.0**3))
initstate[0b000101] = amp
initstate[0b001010] = amp
initstate[0b010000] = amp
initstate[0b011110] = amp
initstate[0b100000] = amp
initstate[0b101110] = amp
initstate[0b110101] = amp
initstate[0b111010] = amp

qc = qsim.QSimulator(6,initstate=initstate,qtrace=True)
# qc.qmeasure([2,1,0])
qc.qgate(qc.Hn(3),[5,4,3])
qc.qmeasure([5,4,3])
