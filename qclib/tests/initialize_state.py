import qclib
import numpy

try:
	prepqbits = numpy.matrix([[0,1],[0,1],[0,1],[0,1]])

	q = qclib.qcsim(5,prepare=prepqbits)
	st = q.qstate()
	fmt = "{:0"+"{:d}".format(q.qsize())+"b}"
	for i in range(len(st)):
		print fmt.format(i), st[i]
except qclib.QClibError, ex:
	print ex.args
