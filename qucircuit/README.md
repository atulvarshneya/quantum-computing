# Installation
Install using pip command -

$ pip install qucircuit

# Core concepts

## Convention for arguments for quantum gates API
* All single qubit gates, such as, X, Y, Z, H, P, UROTk, RND, accept a list of qubits as argument, e.g., circuit.H([3,2,1]) applies hadamard gate to each of these qubits individually. As a shortcut a single integer can also be provided as input argument to apply the gate to that sigle qubit.
* parameterized quantum gates such as phase-rotation gate P, takes the frst argument the phase value, and the second argument is either a list of qubits or a singe qubit index, as mentioned above. E.g., circuit.P(numpy.pi/4,[3,2,1,0]), circuit.P(numpy.pi,3), circuit.UROTk(4,[7,6,5,4])
* Gates that inherently take variable number of qubits as arguments, such as QFT, inputs to those are provided as multiple input arguments, e.g., circuit.QFT(7,6,5,4,3,2,1,0). QFT also accepts a list of qubits as the one argument, e.g., circuit.QFT([i for i in range(8)])
* All control gates take one or more control qubits as arguments. Among all the qubits provided as arguments the last one is the target qubit and all other preceding ones are control qubits. E.g., circuit.CX(ctrl1, ctrl2, ctrl3, target), circuit.CP(numpy.pi/8,control, target).
* Please note the following about control gates. Package qckt.gatesutils allow addition of a control qubit (MSB) to a gate. Note the original gate can be a multi-qubit gate. So it is more accurate to say that all control gates use as many MSBs as control qubits as is per their operation.

## A note about MSB - LSB ordering
qckt as well as qsim follow the convention that when providing arguments to any of the functions the list argument representing qubits or clbits is ordered as [MSB, ...., LSB]. Yes, :-), the [0] element is MSB!

Note that in many gates the order is either explicit, e.g., in CX the arguments are explicitly (control, and target), and in many others it does not matter, e.g., in M the qubits will be measured irrespective of the order. But in some gates, such as QFT it very much *does* matter.

## Using Registers
The use of registers simplifies, and can help in generalizing the quantum circuit.
When writing reusable subroutines the assignment of qubits for various uses, e.g., input, output, needs to be managed carefully across the subroutine and the other program.
While this can be explictly done by passing lists of qubits for each use, and that can definitely serve the purpose very well, the use of registers makes it somewhat more streamlined.

There are two classes of registers - QRegister and CRegister. the former for quantum bits, and the latter for classical bits. The distiction is for assigning the actual qubits and clbits to these registers.

At the end of the day, both the registers are subclasses of list data type. So, operations as indexing (qreg[2]), concatenating (qreg1 + qreg2), etc., can be freely performed on the registers. Just note that the result turns out to be of list data type (not the original QRegister or CRegister type, *this needs to be fixed in subsequent releases*). The assignment of qubits and clbits to the registers follows the MSB...LSB convention as mentioned in the section above.

Example usesof registers:

	import qckt
	inpreg = qckt.QRegister(4)
	outreg = qckt.QRegister(2)
	wrkreg = qckt.QRegister(4)
	clmeas = qckt.CRegister(6)
	# at this stage the registers have been declared, but no specific qubits or clbits have been assigned to them.
 	# For that we use placement()
	nq,nc,placedqu,placedcl = qckt.placement(inpreg,outreg,wrkreg,clmeas)


The above code declares registers and then assigned actual qubits and clbits to them (does the placement of the registers). The way the placement has been done above, the inpreg qubits occupy the MSB locations in the overall number of qubits in the circuit. Followed by outreg and then wrkreg. Since thereis only 1 classical register, it occupies the only number of classical bits in the circuit. Each register has bits assigned in the MSB to LSB order per the convention. So, the order in which the QRegiter objects appear in the placement() arguments, the qubits are assigned in accordance to that. Same for CRegister objects.

	inpreg      outreg   wrkreg
	|9 8 7 6|   |5 4|    |3 2 1 0|

	clmeas
	|5 4 3 2 1 0|

placement() returns 4 values: the first one (nq in the example above) is the total number of qubits required in the circuit; second (nc in the example) is the total number of classical bits required in the circuit. Next two, placedqu and placedcl in the example, are registers containing all qubits and all clbits respectively.

	placedqu
	|9 8 7 6 5 4 3 2 1 0|

	placedcl
	|5 4 3 2 1 0|

the nq and nc should be used while creating the circuit --

	circuit = qckt.QCkt(nq,nc)

# API Documentation

## Package qckt

	class QCkt(nqubits, nclbits=None, name="QCkt")
		Returns an empty quantum circuit

		Methods - Gates:

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

			custom_gate(gatename, op_matrix)
				To add user defined custom gates
				gatename should be per the syntax of a Python variable; op_matrix is the operator matrix in form 
				of numpy.matrix([...],dtype=complex)

			ifcbit(cbit, value)
				Configures the gate object for the operator to be applied only if the mentioned cbit has the 
				mentioned value (0 or 1). ifcbit is not supported by M, Border, and Probe.

				Exampe usage: apply X on qubit 4 only if cbit 2 has value 0.
					import qckt
					ckt = qckt.QCkt(,4)
					ckt.X(4).ifcbit(2,0)

					OR

					import qckt
					ckt = qckt.QCkt(,4)
					xgate = ckt.X(4)
					xgate.ifcbit(2,0)

			Border()
				Places a border in the quantum circuit. Has effect only in the drawing of the circuit

			Probe(header,probestates)
				This is a debuggig aid. Its execution gets skipped on backends which are actual quantum computers.
				header is a string that gets prefixed with "PROBE:" and gets printed as a heading to the probe's
				printout. probestates is either None or a list of states, if None, probe prints amplitude of all 
				the states, else prints the amplitude of only the specified states.

		Methods - circuit operations:

			get_size()
				Returns as a tuple (nqubits, nclbits), the size of quantum and classical registers in the circuit.

			realign(newnq,newnc,inpqubits)
				Creates a potentially larger new circuit from the current circuit with a changed order of the 
				qubits. The original circuitis left intact.
				All the custom gate definitions from the circuit are copied over to the new circuit.
				Returns the new circuit
				Parameters newnq and newnc are the sizes of the new (larger or equal sized) circuit
				inpqubits is a vector that specifies how the old circuit's qubits be replaced in the new circuit
				As an example see the circuits below --
				say,                    current circuit                   new circuit
						q000 ----[H]-[.]----------     q000 --------------------------
							      |                                               
						q001 --------[X]----------     q001 -----------[H]------------
																							 
						q002 ------------[H]------     q002 --------[X]---------------
											     |                
										q003 ---[H]-[.]---------------
	     
				For this realignment, this vector basically answers the questions [q002 -> q?, q001 -> q?, q000 -> q?]
				so, the vector should be [1,2,3], and the realign call should be realign(4,4,[1,2,3])

				In much simpler terms, consider the current circuit as a large gate, and inpqubits vector basically is 
				the way you would use that gate. E.g., CX is defined as MSB = control, LSB as target, but if you 
				want qubit 2 be control and qubit 4 be target, you would say CX(2,4), i.e., inpqubits = [2,4]

			append(othercircuit)
				Creates a new circuit by appending othercircuit to the current circuit. Both the original circuits are 
				left intact.
				Returned circuit qubits match the larger one.  Returned circuit clbits match the larger one.
				All the custom gate definitions from both the circuits are copied over to the new circuit.
				Returns the updated new circuit

			draw()
				Draws a text drawing of the circuit

			list()
				prints out the sequence of gates in the circuit

	class Job 
		Packages the job to be executed on a backend engine.
		Job object converts the circuit to an array of implementation neutral, fully-specified operations (gates, 
		measurement, and probes (for simulator backends))
		Once executed, the backend engine populates the results in the job object.
		job.get_creg() returns an array of Cregister objects from all runs/shots.
		job.get_counts() returns the frequencies of different Cregister values in the results.
		job.get_svec(), only useful for simulator backends, this returns the state-vector at the end of the execution. 
		For simulator backends, shots must be only 1.

		Example Usage:
			import qckt
			import qckt.backend as bknd
			job = qckt.Job(somecircuit, initstate=somestate, prepqubits= None, qtrace=True, shots=100)
			bk_engine = bknd.Qeng() # same as svc.getInstance("qsim") where svc = bknd.Registry().getSvc("QSystems")
			bk_engine.runjob(job)
			print(job.get_creg()[0]) # print the cregister value from the first execution of the circuit
			counts = job.get_counts()
			for i,c in enumerate(counts):
				if c > 0: # lets print only the important ones
					print("{0:04b} ({0:2d})    {1:d}".format(i,c))

# Package qckt.gatesutils

	stretched_opmatrix(nqbits,oper,qbit_list)
		Converts the quantum gate's operator matrix into a matrix for a system with larger number of qubits. 
		The qubits on which the gate operates are kept as the highest order qubits, the additional qubits are 
		left unchanged by the 'stretched' operator.
		
	combine_par(op_list)
		Combines two or more operator matrices into one when they act on separate set of qubits simultaneously.

	combine_seq(op_list)
		Combines two or more operator matrices into one when they act on the same qubits sequentially.

	isunitary(mat)
		Checks if the given operator matrix is unitary or not, returns a boolean (True/False).

	opmat_dagger(opMat)
		returns the transpose conjugate (dagger) of a given operator matrix.

	CTL(opMatrix)
		Utility function to add control bit.

# Package qckt.backend (Backend framework)

	Backend Services Registry
		This is an API for accessing the registry of Quantum Computing Services registered at your installation's 
		configuration. The examples of services that could be registered are IBM quantum computing, Ionq quantum 
		computing, local qsim simulator listSvc() returns a list of tuples (name, description) of all services 
		available (i.e. registered in the installation's configuration) getSvc(svcName) returns handle to the named 
		backend service

		Example usage:
			import qckt.backend as bknd
			reg = bknd.Registry()
			svcTuples = reg.listSvc()
			svc = reg.getSvc("QSystems")

	Backend Service
		Backend service implments the methods to connect with the quantum computing service, using the required 
		authentication/authorization. The service provides methods to discover backend engines under that service, 
		and get the handles to them to run the quantum computing circuits/programs.
		listInstances() returns a list of tuples (name, description) of all instances (quamtum computer) available 
		at this service getInstance(name) returns an object representation of the named instance (quantum computer)

		Example usage: Going through the Registry
			import qckt.backend as bknd
			reg = bknd.Registry()
			svcTuples = reg.listSvc()
			svc = reg.getSvc("QSystems")
			engine_list = svc.listInstances()
			bk_engine = svc.getInstance("local")

		Example usage: Directly accessing the QSystems engines
			import qckt.backend as bknd
			bk_debugging_engine = bknd.Qdeb() # same as svc.getInstance("local")
			bk_engine = bknd.Qeng() # same as svc.getInstance("qsim")

	Backend engines
		The adaptor for the backend needs to interpret the operations sequence in the qckt representation.
		At the end of the job execution (all the shots), the backend adaptor populates the results in the job object, 
		as mentioned above. runjob(job) this is the only function impleented by the backend adaptor. It runs the given 
		job on the backend execution engine. Returns the backend adaptor object itself.

		Example usage: Directly accessing the QSystems engines
			import qckt
			import qckt.backend as bknd
			bk_engine = bknd.Qeng() # same as svc.getInstance("qsim")
			job = qckt.Job(somecircuit, initstate=somestate, shots=100)
			bk_engine.runjob(job)

	class Cregister 
		An object of this class is returned by job.get_creg(), and holds the classical register value got from the measurement 
		operation. It provides method to convert that to pretty printable string, e.g., str(cregister), print(cregister).
		The classical bits array can be accessed through the .value field and its integer value through .intvalue field of the 
		returned object. This class is defined in qckt.backend.BackendAPI

	class StateVector 
		An object of this class is returned by job.get_svec(), and holds the statevector value from the simulator backend engine.
		Note that state is available only when you run on a simulator, not on an actual QC hardware.
		In case of NISQ simulator, the diagonal of the density operator is returned.
		It provides methods to convert that to pretty printable string, e.g., str(statevector), print(statevector).
		The state-vector array can be accessed through the .value field of the object
		The returned object also supports a method StateVector.verbose(boolean), which affects the string conversion such that 
		it includes all states even those with an amplitude of 0. Svec.verbose(boolean) returns the same state-vector object
		This class is defined in BackendAPI.py

