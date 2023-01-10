import sys

class Job:
	'just a packet of all job attributes. Is a qckt concept, so is '
	def __init__(self, circuit, qtrace=False, verbose=False, shots=1):
		'Job is a qckt concept to encapsulate the work packet that is to be submitted to the quantum computer to execute'
		self.circuit = circuit
		self.nqubits, self.nclbits = circuit.get_size()
		self.assembledCkt = circuit.assemble()
		self.qtrace = qtrace
		self.verbose = verbose
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

	def plot_counts(self,verbose=False):
		counts = self.get_counts()
		lc = len(counts)
		nbits = 0
		while 2**nbits < lc: nbits += 1
		if 'ipykernel' in sys.modules:
			lbl = []
			vals = []
			for i,c in enumerate(counts):
				if verbose or c > 0:
					binlbl = ('[{0:0'+str(nbits)+'b}]').format(i)
					lbl.append(str(i)+"\n"+binlbl)
					vals.append(c)
			import matplotlib.pyplot as plt
			fig = plt.bar(lbl,vals)
			for i in range(len(vals)):
				plt.annotate(str(vals[i]), xy=(lbl[i],vals[i]), ha='center', va='bottom')
			plt.show()
		else:
			maxc = max(counts)
			cwid = len(str(maxc))
			scale = 1 if maxc < 50 else 50.0/maxc
			for i,c in enumerate(counts):
				if verbose or c > 0:
					print(('{0:4d} [{0:0'+str(nbits)+'b}]  {1:'+str(cwid)+'d} |').format(i,c),end="")
					for j in range(int(c * scale)):
						print("*",end="")
					print()
		return counts

