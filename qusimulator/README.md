# 1. QUICK START
Install using pip command -

    pip install qusimulator

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

# 2. CORE FUNCTIONS

2.1	**qc = qsim.QSimulator(nqubits, ncbits=None, initstate=None, prepqubits=None, noise_profile=None, qtrace=False, qzeros=False, validation=False, visualize=False)**

First argument specifies the number of qubits in the system. If ncbits is provided it specifies the number of classical bits, if not provide, it defaults to same as the number of qubits. If neither initstate or prepqubits is provided, prepares all qubits to |0>.

Argument 'prepqubits' can be provided to initialize the initial state by providing the states of all individual qubits in the system. The structure to use is a list, example [[a,b],[c,d], ... [x,y]]. Note that [a,b] is the MSB.

Argument 'initstate' can be used to pass an initial state as a numpy.matrix of shape (2**nqubits,1). Also, the initstate should have the amplitudes normalized. See accompanying initialize-state.py for an example. Creating an initstate vector requires more involed coding, but can come in handy when the initial state is required to have very custom distribution of amplitudes - e.g., in case of trying to setup the initial state for testing QFT.

If 'initstate' is provided, any provided 'prepqubits' is ignored. 

If qtrace=True, it causes each gate and measurement operation to emit the resulting state.

If qzeros=True, prints even those whose amplitude is 0.

If validation=True, every qgate() call validates the gate to be unitary

If visualize=True, the qreport() displays an additional bar graph showing the magnitude of the amplitudes of each state.

`QSimulator` version of the simulator ignores the argument, `noise_profile`. For noise simultion use the density matirx based `DMQSimulator` version of the simulator.

**qc = qsim.DMQSimulator(nqubits, ncbits=None, initstate=None, prepqubits=None, noise_profile=None, qtrace=False, qzeros=False, validation=False, visualize=False)**

`DMQSimulator` version of the simulator takes an additional argument, `noise_profile`.

If not `None` its value should be a dictionary object with keys `noise_opseq_init`, `noise_opseq_allgates` and `noise_opseq_qubits`. The values for keys `noise_opseq_init` and `noise_opseq_allgates` are objects either of classes `qsim.noisemodel.NoiseOperator` or `qsim.noisemodel.NoiseOperatorSequence`, or `None`, and value for key `noise_opseq_qubits` is object of class `qsim.noisemodel.NoiseOperatorApplierSequence`, or `None`. More details on `noise_profile` in the section on **Noise Simulation**.

2.2	**qc.qreset()**

Brings the simulator to the same state as after QSimulator() call - initial state, qtrace, qzeros, ... everything.

qreset() has been deprecated. Just re-instantiate the simulator object instead.


2.3	**qc.qgate(quantum_gate, list_of_qubits, noise_chan=None, ifcbit=None, qtrace=False)**

qgate() is used to perform quantum gate operations, quantum_gate, on a set of qubits, list_of_qubits.

There are a number of gates pre-created within the qsim package, and additional gates can be defined by the users (see Section USER DEFINED GATE below). If a gate operates on more than 1 qubit (e.g., CNOT gate, SWAP gate, etc.) then the list in the second argument (list_of_qubits) must contain that many qubits. qgate() validates the number of qubits passed in list_of_qubits against the number of qubits required for the gate, if not correct, throws an exception.

ifcbit argument, if provided, causes the gate to be applied conditionally. ifcbit value is a tuple (cbit, boolval), which essentially implies the gate is appled if the measured classical bit, cbit, value is 0 or is 1 as specified by boolval.

If qtrace is True, the resulting state is printed out.

In `QSimulator` version of the simulator qgate() ignores the argument, `noise_chan`. For noise simultion use the density matirx based `DMQSimulator` version of the simulator.

**qc.qgate(quantum_gate, list_of_qubits, noise_chan=None, ifcbit=None, qtrace=False)**

`DMQSimulator` version of the simulator's `qgate()` method takes an additional argument, `noise_chan`. If not `None` its value should be an object either of classes `qsim.noisemodel.qNoiseChannel` or `qsim.noisemodel.qNoiseChannelSequence`. More details on `noise_chan` in the section on **Noise Simulation**.

2.4 **qc.qnoise(noise_chan, qubits_list, qtrace=False)**

`DMQSimulator` version of the simulator supports `qnoise()` method. This method applies noise as specified by `noise_chan` to `qubits_list` qunits. `noise_chan` is of type `qNoiseChannel` or `qNoiseChannelSequence`.

2.5	**qc.qmeasure(qbit_list, cbit_list=None, qtrace=False)**

Returns the measured values of the qubits in the qubit_list, each 0 or 1, as a list, in the same order as the qubits in the qubit_list. The measured qubits are also read into the corresponding classical bits in the cbit_list. if cbit_list is not specified it defaults to the same list as the qbit_list.

If the bits are in a superposition, the measurement operation will cause the state to randomly collapse to one or the other with the appropriate probability. In this simulator, the Python random.random() function is used to generate the randomness to decide which state to collapse into.

To measure in some basis, you can apply corresponding operation (gate) to the qbits in question, measure, and then apply the inverse of that operation to those qbits.

Cleary, the computations can continue after the measurement operations. Just that the overall state will have the appropriately collapsed state of the measured qubits.

If qtrace is True, the resulting state is printed out.

2.6	**qc.qreport(state=None, header="State", probestates=False)**

Prints the current state of the system. if state argument is provided with a column numpy.matrix, it prints that state instead.
The argument header provides the text to be printed above the state information.
The argument probestates is used to limit the dumping of states information, it gets limited to only the states listed, e.g., probestates=[0,1,2,3]

2.7	**qc.qsnapshot()**

Returns the a python array of all the classical bits and a python array of complex amplitudes of superposition states of the qubits in the system.

2.8	**qc.qsize()**

Returns the number of qubits in the system.

2.9	**qc.qtraceON(boolean)**

Turns ON or OFF printing of state after each qgate() and qmeasure() function call.

2.10	**qc.qzerosON(boolean)**

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

So, using the above created gates as below, you can create 2 entangled |Phi+> bell states, between quits 7,6 and 5,4 --

	qc.qgate(H2,[7,5])
	qc.qgate(C2,[7,6,5,4])


# 5. CREATING USER DEFINED GATES

(see accompanying user_def_gates.py)

Qcsim allows using user defined gates. A user defined gate would be a Python array with two elements [name_string, unitary_matrix]. The element unitary_matrix is the matrix that specifies the gate. It should be created using numpy.matrix([...],dtype=complex), or equivalent. The element name_string is a string that is a user-friendly name of that gate that is used in logs and debug traces.

Here is an example of a simple way for a user to define a CNOT gate in form of a function --

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

If the gate is defined in form of a function, it can take arguments. For instance, for a rotation gate, the rotation angle can be passed as an argument --

	def myR(theta):
		c = numpy.cos(theta)
		s = numpy.sin(theta)
		return ["MY-Rotation({:0.4f})".format(theta), numpy.matrix([[1,0],[0,complex(c,s)]],dtype=complex)]
	qc.qgate(myR(numpy.pi/2),[5])

# 6. ERROR HANDLING, EXCEPTIONS

Various function calls raise exceptions, mostly in cases where user passed arguments are incorrect. The exceptions are raised using class qsim.qSimException.

Following is an example shows how these exceptions are handled --

	import qsim
	try:
		qc = qsim.QSimulator(8)
		qc.qgate(qsim.H(),[0])
		qc.qgate(qsim.C(),[0,9])
	except qsim.QSimError as exp:
		print(exp)

Following is the list of error messages with the name of the function, thrown in an exception --

	(TBD with the latest list)

# 7. COMMAND LINE TOOL qsimcli

Release 1.5.1 adds a simple commandline tool, qsimcli, which provides an interactive way to execute quantum operations. It is more a learning tool than for any serious use. Below is a sample session -

	$ qsimcli
	Type '?' for help.
	> i 4

	Initial State
	0000    1.00000000+0.00000000j
	CREGISTER: 0000
	> h 0

	HADAMARD Qubit[0]
	0000    0.70710678+0.00000000j
	0001    0.70710678+0.00000000j
	CREGISTER: 0000
	> c 0 1

	CNOT Qubit[0, 1]
	0000    0.70710678+0.00000000j
	0011    0.70710678+0.00000000j
	CREGISTER: 0000
	> m 0 1

	MEASURED Qubit[0, 1] = [0, 0] with probability = 0.5
	0000    1.00000000+0.00000000j
	CREGISTER: 0000
	> q
	$

Type a ? to get help, and that is all you will need to know about using the cli. See below.

	$ qsimcli
	Type '?' for help.
	>
	> ?
	Commands:
	  ?                    -- Help
	  help                 -- Help
	  i nqbits             -- Initialize QC
	  m bit1 bit2 ...      -- Measure qubits
	  q                    -- Quit
	Gates:
	  c cbit bit           -- CNOT Gate
	  csw cbit bit1 bit2   -- C-SWAP Gate
	  h bit                -- HADAMARD Gate
	  hn n n-bits ...      -- Simultabeous n-HADAMARD Gates
	  qft n n-bits ...     -- QFT(n) Gate
	  rk k bit             -- ROT(k) Gate
	  rnd bit              -- Random aplitude Gate
	  rphi phi bit         -- ROT(Phi) Gate
	  sqsw bit1 bit2       -- SQ root SWAP gate
	  sw bit1 bit2         -- SWAP Gate
	  t cbit1 cbit2 bit    -- TOFFOLI Gate
	  x bit                -- X Gate
	  y bit                -- Y Gate
	  z bit                -- Z Gate
	> q
	$

# 8. Noise in Quantum Computers

The quantum computers of the current era are described as noisy intermediate-size quantum computers (NISQ computers). Apart from their *intermediate* size in terms of number of qubits, they are also noisy. Noise in quantum computers can introduce classical uncertainty in what the underlying state is. When this happens we need to consider not only a wavefunction but probabilistic sum of wavefunctions when we are uncertain as to which one we have.

For example, if we know that a $\ket{0}$ qubit can flip accidentally with a 20% probability then we would say that there is a 80% probability we have the $\ket{0}$ state and a 20% probability that we have a $\ket{1}$ state. This is called an “impure” or “mixed” state. The mixed state isn’t just one wavefunction but instead a distribution over wavefunctions.

## 8.1 Density Matrix

We represent such a mixed state with something called a density matrix which is a richer representation of quantum states than state vectors. Pure states have very simple density matrices that are written as an outer product of the ket vector representing that state, $\ket{\psi}$, and its complex conjugate $\bra{\psi}$. I.e., the density matrix $\rho_\psi$ is defined as,  $\rho_\psi := \ket{\psi}\bra{\psi}$.

If we want to describe a situation with classical uncertainty between states $\rho_1$ and $\rho_2$, then we can take their weighted sum $(p\rho_1 +(1-p)\rho_2)$, where $p \in [0,1]$ gives the classical probability that the state is $\rho_1$.

## 8.2 Quantum Gate Noise

There are two basic sources of quantum gate noise:

1. **coherent errors** are those that preserve the purity of the input state, i.e., instead of the intended operation $\ket{\psi} \mapsto U \ket{\psi}$ we carry out a perturbed, but unitary operation $\ket{\psi} \mapsto \tilde{U} \ket{\psi}$, where $\tilde{U} \ne U$.
2. **incoherent errors** are those that do not preserve the purity of the input state, in this case we must actually represent the evolution in terms of density matrices. The state $\rho :=\ket{\psi}\bra{\psi}$ is then mapped as $\rho \mapsto \sum_{j=1}^m K_j \rho K_j ^\dagger$, where the operators $K_1,K_2, ..., K_m$ are called Kraus operators and must obey $\sum_{j=1}^m K_j ^\dagger K_j = \boldsymbol{I}$ to conserve the trace of $\rho$. Maps expressed in this form are called Kraus maps. It can be shown that every physical map on a finite dimensional quantum system can be represented as a Kraus map.

**Cuases of incoherent errors:** When a quantum system (e.g., the qubits on a quantum processor) is not perfectly isolated from its environment it generally co-evolves with the environment's degrees of freedom it couples to. The implication is that while the total time evolution of system and environment as a composite can be assumed to be unitary, the system state by itself might not be.

# 9. Noise Simulation in `qusimulator`

`qusimulator` provides a framework to simulate noise in quantum computers. This allows users to design and evaluate the effects of such noise on quantum algorithms without running them on actual quantum hardware.

`DMQSimulator()` version of simulator is density matrix based simulator, and supports noise simulation. The `QSimulator` version and `DMQSimulator are 'drop-in` replacements for each other, except that `QSimulator` ignores all argumetns and method calls related to noise simulation.

`DMQSimulator` supports two mechanims for simulating noise, they can be used individually or together.

1. **Global noise overlay:** a noise profile attached to the simulator which can be setup to add noise automatically at initialization time, and after each quantum gate operation.
2. **Applying noise at specific points in the circuit:** adds noise at specific steps. This is done by passing the `noise_chan` argument in any `qgate()` method calls, and by calling `qnoise()` method at specific instants in the simulation.

## 9.1 Global noise overlay
This mechanism allows the users to pass a noise profile to a `DMQSimulator()` instance. This supports noise to be added at 
1. initialization time 
2. to specific qubits when acted upon by any gates,
3. at all gate operations to the qubits acted upon by the gate

## 9.2 Applying noise at specific points in the circuit

`qc.qnoise(noise_channel, qubits_list)`: this is just like applying a gate, except that instead of a gate operation a noise channel is applied to the specified qubits. The noise channel argument can be either `qNoiseChannel` or `qNoiseChannelSequence` type. . The noise channel should either be a 1-qubit channel, in which case it is 'broadcast' to all the qubits of the `qnoise()` instance, or the number of qubits of the noise channel must match the number of qubits in the `qubits_list` argument.

`qc.qgate(gate, qubits_list, noise_channel)`: this applies the noise channel to the gate instance and the noise channel acts on the same qubits as the gate. The noise channel should either be a 1-qubit channel, in which case it is 'broadcast' to all the qubits of the gate instance, or the number of qubits of the noise channel must match the number of qubits of the gate. 

## Noise channel and noise profile classes

The API uses the following classes to represent the noise channels and the noise profile.

### `qNoiseChannel`, `qNoiseChannelSequence`
`qNoiseChannel` represents one noise channel (a set of operators $K_1, K_2, ..., K_m$ applied as $\sum_{j=1}^m K_j \rho K_j^\dagger$).

The implementation assumes that users might need to apply multiple noise channels as a group in a sequence, the class `qNoiseChannelSequence` allows that in an easy way, it represents a sequence of multiple noise channels applied together, one after the other. All API functions that accept an argument of type `qNoiseChannel` are designed to also accept that argument to be of type `qNoiseChannelSequence`.

### `qNoiseChannelApplierSequence` - noise 'applier' specification.
Typically the noise channels are applied along with a gate operation, so they act on the same qubts as the gate, for those purposes it is sufficient to specify the noise as `qNoiseChannel` or `qNoiseChannelSequence`. However, as part of *noise profile* specification, noise channels can also be applied to specific qubits, this is represented usig the class `NoiseChannelApplierSequence`.

For instance, the noise profile can specify a bit-flip noise on qubits 1 and 2, i.e., to apply this noise after each gate operation involving those qubits. However, if a gate acts on qubits 0 and 1, then after that gate the specified bit-flip noise will be applied to qubit 1  - the qubit common between the gate's target qubits and the noise applier's target qubits. Just to be clear, if the gate acts on qubits other than specified in the applier, that noise in the applier will not be applied.

### `qNoiseProfile`
This class represents the noise profile. It has the following fields -
1. `noise_chan_init` 
	- noise at initialization time 
	- of type `NoiseChannel`, or `NoiseChannelSequence`
2. `noise_chan_qubits` 
	- noise on specific qubits when acted upon by any gates 
	- of type `NoiseChannelApplierSequence`
3. `noise_chan_allgates` 
	- noise at all gate operations to the qubits acted upon by the gate 
	- of type `NoiseChannel`, or `NoiseChannelSequence`
