import qclib
import numpy as np

nqbits = 4

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
def qftop(n):
	opmat = [None]*(2**n)
	for i in range(2**n):
		opmat[i] = rootsofunity(2**n,i)
	opmat = np.matrix(opmat,dtype=complex) / (2**(nqbits/2))
	oper = ["QFT",opmat]
	return oper

try:
	qc = qclib.qcsim(4,qtrace=True)
	for i in range(nqbits):
		qc.qgate(qc.H(),[i])
	qc.qgate(qftop(nqbits), range(nqbits))
	# print qftop(nqbits)
except qclib.QClibError,ex:
	print ex.args
