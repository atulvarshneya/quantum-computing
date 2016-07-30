import qclib
import numpy as np

try:
	q = qclib.qcsim(4,prepare=np.matrix([[1,0],[0,1]],dtype=complex))
	sq2 = np.sqrt(2)
	mybasis = np.matrix([[1/sq2,1/sq2],[1/sq2,-1/sq2]])

	v = q.qmeasure([1],basis=mybasis)
	print v
	q.qreport()
except qclib.QClibError, ex:
	print ex.args
