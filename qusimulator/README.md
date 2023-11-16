# 1. QUICK START

1.2	TUTORIAL INTRODUCTION
--------
(see accompanying helloworld.py)
Lets start with a simple example of using qsim, something like a 'hello world' --

	import qsim
	qc = qsim.QSimulator(8)
	qc.qgate(qsim.H(),[0])
	qc.qgate(qsim.C(),[0,3])
	qc.qreport()
	qc.qmeasure([0])
	qc.qreport()

When run, the above code generates the following output (since measuring randomly collapses to some state per its probability, there is 50% chance you might see the final state as 00000000) --

	State
	00000000    0.70710678+0.00000000j
	00001001    0.70710678+0.00000000j

	State
	00001001    1.00000000+0.00000000j

With respect to the functionality, the above code starts with an 8-qubit system, and then sets up qubits 3 and 0 entangled in bell state |Phi+>. And then measures qubit 0. This is depicted in the diagram below --

	7 -------------------------
	6 -------------------------
	5 -------------------------
	4 -------------------------
	3 -----O-------------------
	2 -----|-------------------
	1 -----|-------------------
	0 -[H]-.-(/)---------------

(Using (/) to depict the measurement operation.)

The output emitted by the above code is the dump of the state right after the setting up of the |Phi+> state, and then after measuring the qubit 0.

Lets go line by line to understand the code --

	import qsim
This first line imports the qsim. Fairly straight forward.

	qc = qsim.QSimulator(8)
The main class in qsim is QSimulator. This line creates an instance of that class. As a convention in this document, qc is always used to represent an instance of the class QSimulator. The QSimulator class instance, qc, represents a quantum computer. The number 8 as the argument to the constructor of class QSimulator, specifies the number of qubits in that quantum computer.

	qc.qgate(qsim.H(),[0])
qgate() is the function that applies a quantum gate on a given set of qubits in the system. In the above line of code, it applies the hadamard gate (H()), to qubit 0. See the documentation below for the gates available.

	qc.qgate(qsim.C(),[0,3])
Here a CNOT gate (C()) is applied on bits 0 and 3, with qubit 0 being the control qubit. In QSimulator the C gate is defined to take the first qubit as the control qubit.

	qc.qreport()
The function qreport() outputs the current superposition state. The first batch of lines is that output.

	qc.qmeasure([0])
The qmeasure() function measures qubit 0.

	qc.qreport()
This last qreport() function call outputs the state after the measurement of the qubit 0.
 
Now, let us run the same code with trace turned on (therefore removed the qreport() calls). Turning trace ON, it outputs the state after init and each gate and measurement steps (see accompanying helloworld_traceON.py) --

	import qsim
	from qgates import *
	qc = qsim.QSimulator(8, qtrace=True)
	qc.qgate(qsim.H(),[0])
	qc.qgate(qsim.C(),[0,3])
	qc.qmeasure([0])
 
and, here is its output --

	Initial State
	00000000    1.00000000+0.00000000j

	HADAMARD Qubit[0]
	00000000    0.70710678+0.00000000j
	00000001    0.70710678+0.00000000j

	CNOT Qubit[0, 3]
	00000000    0.70710678+0.00000000j
	00001001    0.70710678+0.00000000j

	MEASURED Qubit[0] = [0] with probality = 0.5
	00000000    1.00000000+0.00000000j

1.2	PROGRAMMING MODEL
--------
qsim assumes a programming model as shown below.

Users write the algorithms on a front-end classical computer using standard programming language (Python), and qsim provides an API to access and perform operations on a Quantum Computer as a back-end resource.

	                     +--------------------+          +----------------+
	                     |                +---|          |                |
	    +-------+        |                | q |          |                |
	    |       |        |  Classical     | s |          |    Quantum     |
	    |       |--------|  Computer      | i |----------|    Computer    |
	    +-------+        |  (Front-end)   | m |          |   (Back-end)   |
	   /       /         |                |   |          |                |
	  ---------          |                +---|          |                |
	                     +--------------------+          +----------------+

# 2. CORE FUNCTIONS

2.1	**qc = qsim.QSimulator(nqubits, ncbits=None, initstate=None, prepqubits=None, qtrace=False, qzeros=False, validation=False, visualize=False)**

First argument specifies the number of qubits in the system. If ncbits is provided it specifies the number of classical bits, if not provide, it defaults to same as the number of qubits. If neither initstate or prepqubits is provided, prepares all qubits to |0>.

Argument 'prepqubits' can be provided to initialize the initial state by providing the states of all individual qubits in the system. The structure to use is a list, example [[a,b],[c,d], ... [x,y]]. Note that [a,b] is the MSB.

Argument 'initstate' can be used to pass an initial state as a numpy.matrix of shape (2**nqubits,1). Also, the initstate should have the amplitudes normalized. See accompanying initialize-state.py for an example. Creating an initstate vector requires more involed coding, but can come in handy when the initial state is required to have very custom distribution of amplitudes - e.g., in case of trying to setup the initial state for testing QFT.

If 'initstate' is provided, any provided 'prepqubits' is ignored. 

If qtrace=True, it causes each gate and measurement operation to emit the resulting state.

If qzeros=True, prints even those whose amplitude is 0.

If validation=True, every qgate() call validates the gate to be unitary

If visualize=True, the qreport() displays an additional bar graph showing the magnitude of the amplitudes of each state.

2.2	**qc.qreset()**

Brings the simulator to the same state as after QSimulator() call - initial state, qtrace, qzeros, ... everything.

2.3	**qc.qgate(gate_function, list_of_qubits, qtrace=False)**

qgate() is used to perform quantum gate operations on a set of qubits.

There are a number of gates pre-created within the qgates module, and additional gates can be defined by the users (see Section USER DEFINED GATE below). If a gate operates on more than 1 qubit (e.g., CNOT gate, SWAP gate, etc.) then the list in the second argument (list_of_qubits) must contain that many qubits.

The function qgate() validates the number of bits passed in list_of_qubits against the number of qubits required for the gate, if not correct, throws an exception.

If qtrace is True, the resulting state is printed out.

2.4	**qc.qmeasure(qbit_list, cbit_list=None, qtrace=False)**

Returns the measured values of the qubits in the qubit_list, each 0 or 1, as a list, in the same order as the qubits in the qubit_list. The measured qubits are also read into the corresponding classical bits in the cbit_list. if cbit_list is not specified it defaults to the same list as the qbit_list.

If the bits are in a superposition, the measurement operation will cause the state to randomly collapse to one or the other with the appropriate probability. In this simulator, the Python random.random() function is used to generate the randomness to decide which state to collapse into.

To measure in some basis, you can apply corresponding operation (gate) to the qbits in question, measure, and then apply the inverse of that operation to those qbits.

Cleary, the computations can continue after the measurement operations. Just that the overall state will have the appropriately collapsed state of the measured qubits.

If qtrace is True, the resulting state is printed out.

2.5	**qc.qreport(state=None, header="State", probestates=False)**

Prints the current state of the system. if state argument is provided with a column numpy.matrix, it prints that state instead.
The argument header provides the text to be printed above the state information.
The argument probestates is used to limit the dumping of states information, it gets limited to only the states listed, e.g., probestates=[0,1,2,3]

2.6	**qc.qsnapshot()**

Returns the a python array of all the classical bits and a python array of complex amplitudes of superposition states of the qubits in the system.

2.7	**qc.qsize()**

Returns the number of qubits in the system.

2.8	**qc.qtraceON(boolean)**

Turns ON or OFF printing of state after each qgate() and qmeasure() function call.

2.9	**qc.qzerosON(boolean)**

Turns ON or OFF printing of zero amplitude states in trace outputs and qreport() outputs.


# 3. OPERATOR UTILITY FUNCTIONS

3.1	**qsim.qstretch(gate_function, list_of_qubits)**

qstretch takes a gate and an ordered list of qubits on which it would operate and "stretches" it to handle *all* qubits in the system. Basically, the resulting newgate takes as input all the qubits in the system provided as [msb,...,lsb], but performs the original operation only on the given list_of_qubits, and passes through all the other qubits unaffected.

For instance, lets assume we created a 4 qubit system (qsim.QSimulator(4)), and in that we use C gate on qubits 3 and 0 (qgate(C(),[3,0])). Shown on the left side of the figure below. qstretch takes the same arguments and creates a gate that operates on 4 qubits, but still affects only qubits 3 and 0, passing the others through.

                                 +---+
        3 ---.-----          3 --| . |--
             |                   | | |
        2 ---|-----          2 --| | |--
             |                   | | |
        1 ---|-----          1 --| | |--
             |                   | | |
        0 ---O-----          0 --| O |--
                                 +---+

    qc.qgate(C(),[3,0])   ng = qc.qstretch(C(),[3,0])
                         qc.qgate(ng,[3,2,1,0])

qstretch() is useful in cases where you want to make a 'blackbox' function which does an equivalent of a series of operations in one go (see the accompanying bern_vazy.py). To do that you would typically use qcombine_seq()'s and qcombine_par()'s in conjunction with qstretch()'s.

3.2	**qsim.qinverse(op,name=None)**

Returns the inverse of the operator. If name argument is not provided, it generates a name by prefixing the name of the provided operator with "INV-"

3.3	**qsim.qisunitary(op)**

Checks if the provided operator is unitary opperator or not. Returns boolean value (True or False).

# 4. Gates in qsim

4.1	PRE-DEFINED GATES
--------
A number of gates are pre-defined in the QSimulator class. The following is the list --

	H()		Hadamard gate
	X()		Pauli_x gate
	Y()		Pauli_y gate
	Z()		Pauli_z gate
	R(phi)		Phase rotation by phi
	Rk(k)		Phase rotation by 2*pi/(2**k), useful in QFT algorithm
	C()		CNOT gate
	SWAP()		SWAP gate
	CSWAP()		Controlled-SWAP gate
	SQSWAP()	Square root of SWAP gate
	T()		TOFFOLI gate
	Hn(n)		Hadamard gates applied on n qubits, added since it is commonly used
	QFT(n)		QFT gate for n qubits
	RND()		Randomizes the qubit - useful for testing some cases

4.2	CONTROLLED GATES
--------
CTL(op,name=None)
	Build a controlled gate from any gate, MSB position as control bit. Can apply CTL() multiple times e.g., CTL(CTL(op)), to add multiple control qubits.

Examples:
	C() is the same as qsim.CTL(qsim.X(),name="CNOT")
	T() is the same as qsim.CTL(qsim.CTL(qsim.X()),name="TOFFOLI")

4.3 OPERATOR UTILITY FUNCTIONS
--------

4.3.1 **qsim.qcombine_seq(name, op_list)**

Combines a sequential application of gates into one equivalent gate. The argument name is the name of the resulting gate. Argument op_list is a list of gates each of the structure [name,matrix].

	--[A]--[B]--[C]--[D]--    ==>   --[G]--
 
To combine the above 

	G = qsim.qcombine_seq("SEQ",[A,B,C,D])
 
and to use it, for instance to apply it on qubit 2 
 
	qc.qgate(G,[2])

4.3.2 **qsim.qcombine_par(name, op_list)**

Combines a parallel application of gates into one equivalent gate. The argument name is the name of the resulting gate. Argument op_list is a list of gates.

	                         +-+
	3 --[A]----          3 --| |--
	2 --[B]----     ==>  2 --| |--
	1 --[C]----          1 --|G|--
	0 --[D]----          0 --| |--
	                         +-+

To combine the above into one operation with 4 qubits as inputs 

	G = qsim.qcombine_par("PAR",[A,B,C,D])
 
and to use it, for example to apply it on qubits 7,5,3,1 

	qc.qgate(G,[7,5,3,1])
 
An illustrative example is 

	                         +--+
	1 --[H]----          1 --|  |--
	                         |H2|
	0 --[H]----          0 --|  |--
	                         +--+
	H2 = qsim.qcombine_par("H2",[qsim.H(),qsim.H()])

	                         +--+
	3 ---.-----          3 --|  |--
	     |                   |  |
	2 ---O-----          2 --|  |--
	                         |C2|
	1 ---.-----          1 --|  |--
	     |                   |  |
	0 ---O-----          0 --|  |--
	                         +--+
	C2 = qsim.qcombine_par("C2",[qsim.C(),qsim.C()])

Create 2 entangled |Phi+> bell states, between quits 7,6 and 5,4 using these --

	qc.qgate(H2,[7,5])
	qc.qgate(C2,[7,6,5,4])


# 5. CREATING USER DEFINED GATES

(see accompanying user_def_gates.py)

Qcsim allows using user defined gates. A user defined gate would be written as a function that returns a Python array with two elements [name_string, unitary_matrix]. The element unitary_matrix is the matrix that specifies the gate. It should be created using numpy.matrix([...],dtype=complex), or equivalent. The element name_string is a string that is a user-friendly name of that gate that is used in logs and debug traces.

Here is an example of a simple way for a user to define a CNOT gate --
	def myCNOT():
		return ["MY-CNOT", numpy.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)]

As shown in the code above, while writing the unitary_matrix for myCNOT we assumed as if the entire system has only 2 qubits.

Now, since in this definition of CNOT the higher order qubit (MSB) is the controlling qubit, hence when applying this gate to any two qubits, say, 4 and 7, where say, bit 4 is the controlling qubit, the qgate() function would be invoked as --

	qc.qgate(myCNOT(),[4,7])

Or, if qubit 7 is to be the controlling qubit, then as --

	qc.qgate(myCNOT(),[7,4])

Qclib does all the trickery required to convert the gate matrix to handle all the qubits of the system, and performing the gate operation only on the speciic qubits.

So, in general, if the gate operates on n qubits, then it should be written as if the entire system consists of only n qubits, and when calling qgate(), the order of qubits should be [MSB, ..., LSB].

The system looks at the size of the matrix specifying the gate to determine the number of qubits required for that gate. If the number is incorrect, it throws an exception.

Since the gate is defined in form of a function, it can take arguments. For instance, for a rotation gate, the rotation angle can be passed as an argument --

	def myR(theta):
		c = numpy.cos(theta)
		s = numpy.sin(theta)
		return ["MY-Rotation({:0.4f})".format(theta), numpy.matrix([[1,0],[0,complex(c,s)]],dtype=complex)]
	qc.qgate(myR(numpy.pi/2),[5])
 
(Note: To see some change in the state, perform an X() or H() or some such on the qubit before the phase rotation.)


# 6. ERROR HANDLING, EXCEPTIONS

Various function calls raise exceptions, mostly in cases where user passed arguments are incorrect. The exceptions are raised using class qsim.qSimException.

Following is an example shows how these exceptions are handled --

	import qsim
	from qSimException import *
	try:
		qc = qsim.QSimulator(8)
		qc.qgate(qsim.H(),[0])
		qc.qgate(qsim.C(),[0,1])
	except qSimException as exp:
		print(exp.args)

Following is the list of error messages with the name of the function, thrown in an exception --

	(TBD with the latest list)
