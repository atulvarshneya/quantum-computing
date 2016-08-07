import qclib
import numpy as np

try:
	nqbits = 6

	# initialise with the default state of all qbits = |0>
	q = qclib.qcsim(nqbits,qtrace=True)

	# initialise with initial states of qbits
	q = qclib.qcsim(nqbits,prepqubits=[[1,0],[1,0],[1,0],[0,1],[1,0],[0,1]],qtrace=True)
	q.qgate(q.X(),[0])

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
	q = qclib.qcsim(nqbits,initstate=initstate, qtrace=True)

except qclib.QClibError, ex:
	print ex.args
