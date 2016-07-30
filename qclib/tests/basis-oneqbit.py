import qclib
import numpy as np

try:
	init = np.transpose(np.matrix([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],dtype=complex))
	q = qclib.qcsim(4, initstate=init)
	sq2 = np.sqrt(2)
	mybasis = np.matrix([[1/sq2,1/sq2],[1/sq2,-1/sq2]])

	v = q.qmeasure([1],basis=mybasis)
	print v
	q.qreport()
except qclib.QClibError, ex:
	print ex.args
