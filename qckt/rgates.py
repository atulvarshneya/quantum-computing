
class Rx(QGate):
	def __init__(self, theta, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [theta]
		self.name = "Rx"

		rot = self.gateparams[0]
		ck = np.cos(rot/2))
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(0,-sk)], [complex(0,-sk),complex(ck,0)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"Rx")
		return self

	def check_qbit_args(self,nqbits):
		return self.oneqbit_args(nqbits)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

class CRx(QGate):
	def __init__(self, theta, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [theta]
		self.name = "CRx"

		rot = self.gateparams[0]
		ck = np.cos(rot/2))
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(0,-sk)], [complex(0,-sk),complex(ck,0)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"])
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Rx"])
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):


class Ry(QGate):
	def __init__(self, theta, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [theta]
		self.name = "Ry"

		rot = self.gateparams[0]
		ck = np.cos(rot/2))
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(-sk,0)], [complex(sk,0),complex(ck,0)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"Ry")
		return self

	def check_qbit_args(self,nqbits):
		return self.oneqbit_args(nqbits)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

class CRy(QGate):
	def __init__(self, theta, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [theta]
		self.name = "CRy"

		rot = self.gateparams[0]
		ck = np.cos(rot/2))
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,0),complex(-sk,0)], [complex(sk,0),complex(ck,0)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"])
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Ry"])
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):


class Rz(QGate):
	def __init__(self, theta, qbit):
		super().__init__()
		self.qbits = [qbit]
		self.gateparams = [theta]
		self.name = "Rz"

		rot = self.gateparams[0]
		ck = np.cos(rot/2))
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,-sk),complex(0,0)], [complex(0,0),complex(ck,sk)]],dtype=complex)

	def addtocanvas(self,canvas):
		canvas._add_simple(self.qbits[0],"Rz")
		return self

	def check_qbit_args(self,nqbits):
		return self.oneqbit_args(nqbits)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

class CRz(QGate):
	def __init__(self, theta, *allqbits):
		super().__init__()
		self.qbits = list(allqbits)
		self.gateparams = [theta]
		self.name = "CRz"

		rot = self.gateparams[0]
		ck = np.cos(rot/2))
		sk = np.sin(rot/2)
		self.opMatrix = np.matrix([ [complex(ck,-sk),complex(0,0)], [complex(0,0),complex(ck,sk)]],dtype=complex)
		for q in range(len(self.qbits)-1):
			self.opMatrix = gutils.CTL(self.opMatrix)

	def addtocanvas(self,canvas):
		# canvas._add_simple(self.qbits,[".","UROTk"])
		canvas._add_connected(self.qbits,["."]*(len(self.qbits)-1)+["Rz"])
		return self

	def check_qbit_args(self,nqbits):
		return self.varqbit_args(nqbits,2)

	# INHERIT def realign(self,newseq):
	# INHERIT def __str__(self):

