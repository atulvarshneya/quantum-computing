import qsim
import numpy as np

try:
	init = np.transpose(np.matrix([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],dtype=complex))
	q = qsim.QSimulator(4, initstate=init)
	sq2 = np.sqrt(2)
	mybasis = ["MY BASIS",np.matrix([[1.0/sq2,1.0/sq2],[1.0/sq2,-1.0/sq2]],dtype=complex)]

	v = q.qmeasure([1],basis=mybasis)
	print(v)
	q.qreport()
except qsim.QSimError as ex:
	print(ex.args)
