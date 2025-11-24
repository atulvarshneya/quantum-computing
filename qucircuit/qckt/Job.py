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

	def get_counts(self, register=None):
		if register is not None:
			# register specifies which classical register to get counts for
			# for now, only single classical register is supported
			for bit in register:
				if bit < 0 or bit >= self.nclbits:
					raise ValueError("Invalid classical register specified")
				if sum([1 if bit == b else 0 for b in register]) > 1:
					raise ValueError("Duplicate bits in classical register specified")
			mask = 0
			for bit in register:
				mask |= (1 << bit)
			counts = {}
			for i in sorted(self.result.creg_counts.keys()):
				c = self.result.creg_counts[i]
				state = i & mask
				counts[state] = counts.get(state,0) + c
			return counts
		else:
			# just to have the keys in a sorted order
			counts = {}
			for i in sorted(self.result.creg_counts.keys()):
				counts[i] = self.result.creg_counts[i]
			return counts

	def plot_counts(self,register=None, verbose=False):
		counts = self.get_counts(register=register)
		if 'ipykernel' in sys.modules:
			lbl = []
			vals = []
			for i in range(2**self.nqubits):
				c = counts.get(i,0)
				if verbose or c > 0:
					binlbl = ('[{0:0'+str(self.nqubits)+'b}]').format(i)
					lbl.append(str(i)+" "+binlbl)
					vals.append(c)
			import matplotlib.pyplot as plt
			plt.xticks(rotation='vertical')
			fig = plt.bar(lbl,vals)
			for i in range(len(vals)):
				plt.annotate(str(vals[i]), xy=(lbl[i],vals[i]), ha='center', va='bottom')
			plt.show()
		else:
			maxc = max([val for k,val in counts.items()])
			cwid = len(str(maxc))
			scale = 1 if maxc < 50 else 50.0/maxc
			for i in range(2**self.nqubits):
				c = counts.get(i,0)
				if verbose or c > 0:
					print(('{0:4d} [{0:0'+str(self.nqubits)+'b}]  {1:>'+str(cwid)+'d} |').format(i,c),end="")
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
		# print(f'Total Time :  {tot_time:9.4f} sec')
		print(f'Per Operation:')
		for op in op_counts.keys():
			# print(f'    {op:8s} {op_times[op]:9.4f} sec  {op_counts[op]:4d} times {op_times[op]/op_counts[op]:4.4f} avg')
			print(f'    {op:8s} {op_counts[op]:4d} times')

