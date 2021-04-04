# Reference

Convention for arguments for quantum gates API
---
* All single qubit gates, such as, X, Y, Z, H, P, UROTk, RND, accept a list of qubits as argument, e.g., circuit.H([3,2,1]) applies hadamard gate to each of these qubits. As a shortcut a single integer can also be provided as input argument to apply the gate to that sigle qubit.
* parameterized quantum gates such as phase-rotation gate P, takes teh frst argument the phase value, and teh second argument is either a list of qubits or a singe qubit index, as mentioned above. E.g., circuit.P(numpy.pi/4,[3,2,1,0]), circuit.P(numpy.pi,3), circuit.UROTk(4,[7,6,5,4])
* All control gates take one or more control qubits as arguments. Among all the qubits provided as arguments the last one is the target qubit and all other preceding ones are control qubits. E.g., circuit.CX(ctrl1, ctrl2, ctrl3, target), circuit.CP(numpy.pi/8,control, target).
* Gates that inherently take variable number of qubits as arguments, such as QFT, inputs to those are provided as multiple input arguments, e.g., circuit.QFT(7,6,5,4,3,2,1,0). As a shortcut, QFT also accepts a list of qubits as the one argument, e.g., circuit.QFT([i for i in range(8)])


A note about MSB - LSB ordering
---
qckt as well as qsim follow the convention that when providing arguments to any of the functions the list argument representing qubits or clbits is ordered as [MSB, ...., LSB]. Yes, :-), the [0] element is MSB!

Note that in many gates the order is either explicit, e.g., in CX the arguments are explicitly (control, and target), or does not matter, e.g., in M the qubits will be measured irrespective of the order. But in some gates, such as QFT it very much *does* matter.

API Documentation
---
QCkt
---
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
	custom_gate(gatename, op_matrix)
		To add user defined custom gates
		gatename should be per the syntax of a Python variable; op_matrix is the operator matrix in form of numpy.matrix([...],dtype=complex)
	get_size()
		Returns the size of quantum and classical registers as a a tuple (nqubits, nclbits)
	realign(newnq,newnc,inpqubits)
		Creates a potentially larger new circuit from the current circuit with a changed order of the qubits. The original circuitis left intact.
		All the custom gate definitions from the circuit are copied over to the new circuit.
		Returns the new circuit
		Parameters newnq and newnc are the sizesof the new (larger or equal sized) circuit
		inpqubits is a vector that specifies how the old circuit's qubits be replaced in the new circuit
		As an example see the circuits below --
		say,                    current circuit                   new circuit
		               q000 ----[H]-[.]----------     q000 --------------------------
		                             |                                               
		               q001 --------[X]----------     q001 -----------[H]------------
		                                                                             
		               q002 ------------[H]------     q002 --------[X]---------------
		                                                            |                
		                                              q003 ----[H]-[.]---------------
		For this realignment, this vector basically answers the questions [q002 -> q?, q001 -> q?, q000 -> q?]
		so, the vector should be [1,2,3], and the realign call should be realign(4,4,[1,2,3])

		In much simpler terms, consider the current circuit as a large gate, and inpqubits vector basically is 
		the way you would use that gate. E.g., CX is defined as MSB = control, LSB as target, but if you 
		want qubit 2 be control and qubit 4 be target, you would say CX(2,4), i.e., inpqubits = [2,4]

	append(othercircuit)
		Creates a new circuit by appending othercircuit to the current circuit. Both the original circuits are left intact.
		Returned circuit qubits match the larger one.  Returned circuit clbits match the larger one.
		All the custom gate definitions from both the circuits are copied over to the new circuit.
		Returns the updated new circuit
	draw()
		Draws a text drawing of the circuit

Backend
---
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
