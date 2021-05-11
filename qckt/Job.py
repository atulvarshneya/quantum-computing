
class Job:
	'just a packet of all job attributes. Is a qckt concept, so is '
	def __init__(self, circuit, initstate=None, prepqubits=None, qtrace=False, shots=1):
		'Job is a qckt concept to encapsulate the work packet that is to be submitted to the quantum computer to execute'
		self.circuit = circuit
		self.nqubits, self.nclbits = circuit.get_size()
		self.assembledCkt = circuit.assemble()
		self.initstate = initstate
		self.prepqubits = prepqubits
		self.qtrace = qtrace
		self.shots = shots
		# result will be populated after the job is run
		self.result = None

	def get_svec(self):
		return self.result.state_vector

	def get_creg(self):
		return self.result.cregister

	def get_counts(self):
		counts = [0]*(2**self.nclbits)
		for r in self.result.cregister:
			counts[r.intvalue] += 1
		return counts


