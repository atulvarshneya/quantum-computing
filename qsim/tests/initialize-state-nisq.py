import NISQsim
import qgates
from qSimException import *
import numpy as np

try:
	nqbits = 6

	# initialise with the default state of all qbits = |0>
	q = NISQsim.QSimulator(nqbits,qtrace=True)
	q.qgate(qgates.H(),[1])
	q.qgate(qgates.C(),[1,0])

	# initialise with initial states of qbits
	q = NISQsim.QSimulator(nqbits,prepqubits=[[1,0],[1,0],[1,0],[0,1],[1,0],[0,1]],qtrace=True)
	q.qgate(qgates.H(),[1])
	q.qgate(qgates.C(),[1,0])

	# or build the full state yourself (good if you need a very custom state, e.g., for testing QFT)
	initstate = [None]*(2**nqbits)
	p = 0
	stsz = 2**nqbits
	for i in range(stsz):
		c = np.cos(i*2*np.pi/stsz)
		s = np.sin(i*2*np.pi/stsz)
		initstate[i] = complex(c,s)
		p += np.absolute(initstate[i])**2
	initstate = np.transpose(np.matrix(initstate,dtype=complex))/np.sqrt(p)
	q = NISQsim.QSimulator(nqbits,initstate=initstate, qtrace=True)
	q.qgate(qgates.H(),[1])
	q.qgate(qgates.C(),[1,0])

except QSimError as ex:
	print(ex.args)
