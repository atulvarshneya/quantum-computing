Reference

MSB - LSB ordering:
	qcckt as well as qclib follow the convention that when providing arguments to any of the functions 
	the list argument representing qubits or clbits is ordered as [MSB, ...., LSB].
	Yes, :-), the [0] element is MSB!
	Note that in many gates the order is either explicit, e.g., in CX the arguments are explicitly (control, and target),
	or does not matter, e.g., in M the qubits will be measured irrespective of the order. But in some gates, such as QFT 
	it very much *does* matter.

QCkt
	QCkt(nqubits, nclbits=None, name="QCkt")
		Returns an empty quantum circuit
	CX(control, target)
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
	T(control1, control2, target)
		Appends a TOFFOLI gate to the quantum circuit
		Returns the updted quantum circuit
	M(qubitslist, clbitslist=None)
		Appends MEASUREMENT gates for measuring given qubits list into classical bits list
		Returns the updted quantum circuit
	QFT(qubitslist)
		Appends a QFT gate across the given qubits list
		The drawn circuit depicts multiple QFT gates, but it is 1 QFT gate acting on those qubits
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
		Returns a handle object to a backend execution environment (a local qc simulator)
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
	get_creg()
		Returns the result classical bits register object
		The classical bits array can be accessed through the .value field of the returned object
