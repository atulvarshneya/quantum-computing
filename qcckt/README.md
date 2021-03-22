Reference

QCkt
	QCkt(nqubits, nclbits=None, name="QCkt")
		Returns an empty quantum circuit
	C(ctrl, target)
		Appends a CNOT gate to the quantum circuit
		Returns the updted quantum circuit
	H(qubit)
		Appends a HADAMARD gate to the quantum circuit
		Returns the updted quantum circuit
	X(qubit)
		Appends a NOT gate to the quantum circuit
		Returns the updted quantum circuit
	Y(qubit)
		Appends a PAULI-Y gate to the quantum circuit
		Returns the updted quantum circuit
	Z(qubit)
		Appends a PAULI-Z gate to the quantum circuit
		Returns the updted quantum circuit
	T(ctl1, ctl2, target)
		Appends a TOFFOLI gate to the quantum circuit
		Returns the updted quantum circuit
	M(qubitslist, clbitslist=None)
		Appends MEASUREMENT gates for measuring given qubits list into classical bits list
		Returns the updted quantum circuit
	Border()
		Places a border in the quantum circuit. Has effect only in the drawing of the circuit
	get_size()
		Returns the size of quantum and classical registers as a a tuple (nqubits, nclbits)
	realign(newnq,newnc,inpqubits)
		Creates a new circuit from the current circuit with a changed order of the qubits
		Returns the new circuit
	append(othercircuit)
		Append a circuit to the current circuit.
		Returned circuit qubits match the larger one.
		Returned circuit clbits match the larger one.
		Returns the updated circuit
	draw()
		Draws a text drawing of the circuit
Backend
	Backend()
		Returns a handle object to a backend execution environment
	run(circuit, initstate=None, prepqubits=None, qtrace=False)
		Runs the given circuit on the backend execution environment
		Initial state can be passed inform of state vector, or list of prepared qubits
		The results of the execution are stored in the environment handle object
		Returns the same backend environment handle object
	get_svec()
		returns the result state-vector object
		The state-vector array can be accessed through the .value field of the returned object
		The returned object supports conversion to string representation for pretty printing
		That handle supports a method svec.verbose(boolean), and returns the same handle
	def get_creg(self)
		Returns the result classical bits register object
		The classical bits array can be accessed through the .value field of the returned object
