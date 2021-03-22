Reference

QCkt
	Constructor -- QCkt(nq, nc=None, name="QCkt"):
		C(ctrl, target):
		H(qubit):
		X(qubit):
		Y(qubit):
		Z(qubit):
		T(ctl1, ctl2, target):
		M(qbits, cbits=None):
		Border():
		realign(newnq,newnc,inpqubits): # change the qubits order to a different order
		Operator '+'
		draw():
Backend
	def Backend()
	def run(self, circuit, initstate=None, prepqubits=None, qtrace=False):
	def get_svec(self):
	def print_svec(self):
	def get_creg(self):
