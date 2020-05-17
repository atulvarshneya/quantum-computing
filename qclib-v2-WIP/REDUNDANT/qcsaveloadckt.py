
## Is this even required?????

	##########################################################
	## save and load circuits (nqubits, custum gates, circuit
	## Is it even required????
	##########################################################
	def save(self,dirname):
		if not os.path.isdir(dirname):
			os.mkdir(dirname)
		fname = dirname+"/config"
		with open(fname, "wt") as f:
			# first entry in config is nqubits
			f.write("{}".format(self.nqubits))
			# second entry - none yet
			pass
		fname = dirname+"/gates"
		with open(fname, "wt") as f:
			## TODO
			pass
		fname = dirname+"/circuit"
		with open(fname, "wt") as f:
			for g in self.ckt:
				f.write("{}".format(g[0]))
				for q in g[2]:
					f.write("|{}".format(q))
				f.write("\n")

	def load(self, dirname):
		if not os.path.isdir(dirname):
			raise QCError("Directory not accessible: {}".format(dirname))
		self.nqubits = 0
		fname = dirname+"/config"
		with open(fname, "rt") as f:
			# first entry in config is nqubits
			nq = f.readline()
			self.nqubits = int(nq)
			# second entry - none yet
			pass
		fname = dirname+"/gates"
		with open(fname, "rt") as f:
			## TODO
			pass
		self.ckt = []
		fname = dirname+"/circuit"
		with open(fname, "rt") as f:
			for line in f:
				toks = line.split("|")
				gtname = toks[0]
				qubits = []
				for q in toks[1:]:
					qubits.append(int(q))
				self.add(gtname, qubits)

