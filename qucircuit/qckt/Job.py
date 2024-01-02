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
		self.runstats = None

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
					lbl.append(str(i)+" "+binlbl)
					vals.append(c)
			import matplotlib.pyplot as plt
			plt.xticks(rotation='vertical')
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

	def get_runstats(self):
		return self.runstats

	def print_runstats(self):
		qsteps = self.runstats['QSteps']
		op_counts = self.runstats['OpCounts']
		op_times = self.runstats['OpTimes']
		tot_time = 0.0
		for k,v in op_times.items():
			tot_time = tot_time + v
		print(f'Total Ops  :  {qsteps:4d}      operations')
		print(f'Total Time :  {tot_time:9.4f} sec')
		print(f'Per Operation:')
		for op in op_counts.keys():
			print(f'    {op:8s} {op_times[op]:9.4f} sec  {op_counts[op]:4d} times {op_times[op]/op_counts[op]:4.4f} avg')

