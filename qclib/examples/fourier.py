import qclib
import numpy as np

nqbits = 8

try:
	# setup an initial state to try out QFT
	initstate = [None]*(2**nqbits)
	p = 0
	stsz = 2**nqbits
	for i in range(stsz):
		if (i % (stsz/8)) == 0:
			initstate[i] = 1
		else:
			initstate[i] = 0
		p += np.absolute(initstate[i])**2
	initstate = np.transpose(np.matrix(initstate,dtype=complex))/np.sqrt(p)

	# Start the Quantum Computer Simulator
	q = qclib.qcsim(nqbits,initstate=initstate, qtrace=True)
	q.qtraceON(True)
	q.qzerosON(False)

	qftgate = q.QFT(nqbits)
	if not q.qisunitary(qftgate):
		print ">>>>>> NOT UNITARY!!!",qfgate[0]
	else:
		print "Is Unitary.",qftgate[0]
	lst = range(nqbits)
	lst.reverse()
	q.qgate(qftgate, lst)

except qclib.QClibError,ex:
	print ex.args
