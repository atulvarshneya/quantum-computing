import qclib
import numpy as np

nqbits = 10

# create a list of nth roots of unity
def rootsofunity(n,step):
	rootlist = [None]*n
	theta = 2 * np.pi / n
	for i in range(n):
		pow = i * step
		pow = pow % n
		# e^(2*pi/n)*pow
		c = np.cos(theta*pow)
		s = np.sin(theta*pow)
		rootlist[i] = complex(c,s)
	return rootlist

# ... and using that, create the QFT operator for the given number of qbits
def qft(n):
	opmat = [None]*(2**n)
	for i in range(2**n):
		opmat[i] = rootsofunity(2**n,i)
	opmat = np.matrix(opmat,dtype=complex) / (2**(nqbits/2))
	oper = ["QFT",opmat]
	return oper

try:
	# setup an initial state to try out QFT
	initstate = [None]*(2**nqbits)
	p = 0
	stsz = 2**nqbits
	for i in range(stsz):
		initstate[i] = i%8
		p += np.absolute(initstate[i])**2
	initstate = np.transpose(np.matrix(initstate,dtype=complex))/np.sqrt(p)

	# Start the Quantum Computer Simulator
	q = qclib.qcsim(nqbits,initstate=initstate, qtrace=True, qzeros=True)
	q.qzerosON(False)

	qftgate = qft(nqbits)
	if not q.qisunitary(qftgate):
		print ">>>>>> NOT UNITARY!!!",qfgate[0]
	else:
		print "Is Unitary.",qftgate[0]
	lst = range(nqbits)
	lst.reverse()
	q.qgate(qftgate, lst)
except qclib.QClibError,ex:
	print ex.args
