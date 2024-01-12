# Installation
Install using pip command -

    pip install qucircuit

# Basic concepts

## Convention for arguments for quantum gates API
* All gates accept qubits as a 'flat' list of qubits as arguments per the number of qubits it acts on. E.g., Tiffoli gate acting on qubits 0, 1, and 2, is invoked as `circuit.CCX(0,1,2)`; and QFT which accepts a variable number of qubits is invoked as `circuit.QFT(7,6,5,4,3,2,1,0)` to act on these 8 qubits 7 ... 0. Note, if the qubits are stored as lists, they can be provided as argument using the *list argument, such as `circuit.QFT(*list)`
* All single qubit gates, such as, `X`, `Y`, `Z`, `H`, `P`, `UROTk`, `RND`, also accept a list of qubits as a mchanism of 'broadcasting' the gate to all those qubits. E.g., `circuit.H([3,2,1])` applies hadamard gate to each of these qubits individually.
* Parameterized quantum gates such as phase-rotation gate, `P`, takes the frst argument the phase value, and the second argument as the target qubit; and as mentioned above the second argument can also be a list of qubits. E.g., `circuit.P(numpy.pi/4,3)`, `circuit.P(numpy.pi/4,[3,2,1,0])`, `circuit.UROTk(4,[7,6,5,4])`
* All control gates take one or more control qubits as arguments. Among all the qubits provided as arguments the target qubit(s) are the LSB(s) and all other preceding ones are control qubits. E.g., `circuit.CX(ctrl1, ctrl2, ctrl3, target)`, `circuit.CP(numpy.pi/8,control, target)`. Specifically, a controlled single-qubit gate will have the target qubit as the lowest LSB, and, for instance, a controlled 2-qubit gate will have target qubits as the lowest 2 LSBs.

## A note about MSB - LSB ordering
`qckt`, as well as `qsim`, follow the convention that when providing arguments to any of the functions the list argument representing `qubits` or `clbits` is ordered as `[MSB, ...., LSB]`. Yes, :-), the 0th index element is MSB!

Note that in many gates the order is either explicit, e.g., in `CX` the arguments are explicitly (control, and target), and in some others it does not matter, e.g., in `M` the qubits will be measured with the same outcome irrespective of the order. But in some gates, such as `QFT` it very much *does* matter.

## Using Registers (Registers are being deprecated, use python lists instead)
The use of registers simplifies, and can help in readability of the quantum circuit.

When writing reusable subroutines the assignment of qubits for various uses, e.g., input, output, needs to be managed carefully across the subroutine and the other program. While this can be explictly done by passing lists of qubits for each use, and that can definitely serve the purpose very well, the use of registers makes it easier to read.

There are two classes of registers - `QRegister` and `CRegister`. the former for quantum bits, and the latter for classical bits. The distiction is for assigning the actual `qubits` and `clbits` to these registers.

At the end of the day, both the registers are subclasses of `list` data type. So, operations as indexing (`qreg[2]`), concatenating `(qreg1 + qreg2)`, etc., can be freely performed on the registers. Just note that the result turns out to be of `list` data type (not the original `QRegister` or `CRegister` type, *this will be fixed in subsequent releases*). The assignment of qubits and clbits to the registers follows the MSB...LSB convention as mentioned in the section above.

Example uses of registers:

	import qckt
	inpreg = qckt.QRegister(4)
	outreg = qckt.QRegister(2)
	wrkreg = qckt.QRegister(4)
	clmeas = qckt.CRegister(6)
	# at this stage the registers have been declared, but no specific qubits or clbits have been assigned to them.
 	# For that we use placement()
	nq,nc,placedqu,placedcl = qckt.placement(inpreg,outreg,wrkreg,clmeas)


The above code declares registers and then assigned actual `qubits` and `clbits` to them (does the placement of the registers). The way the placement has been done above, the `inpreg` qubits occupy the MSB locations in the overall number of qubits in the circuit. Followed by `outreg` and then `wrkreg`. Since there is only 1 classical register, it occupies the only number of classical bits in the circuit. Each register has bits assigned in the MSB to LSB order per the convention. So, the order in which the `QRegiter` objects appear in the `placement()` arguments, the qubits are assigned in accordance to that. Same for `CRegister` objects.

	inpreg      outreg   wrkreg
	|9 8 7 6|   |5 4|    |3 2 1 0|

	clmeas
	|5 4 3 2 1 0|

`placement()` returns 4 values: the first one (`nq` in the example above) is the total number of qubits required in the circuit; second (`nc` in the example) is the total number of classical bits required in the circuit. Next two, `placedqu` and `placedcl` in the example, are registers containing all `qubits` and all `clbits` respectively.

	placedqu
	|9 8 7 6 5 4 3 2 1 0|

	placedcl
	|5 4 3 2 1 0|

the `nq` and `nc` should be used while creating the circuit --

	circuit = qckt.QCkt(nq,nc)

# Noise in Quantum Computers

The quantum computers of the current era are described as noisy intermediate-size quantum computers (NISQ computers). Apart from their *intermediate* size in terms of number of qubits, they are also noisy. Noise in quantum computers can introduce classical uncertainty in what the underlying state is. When this happens we need to consider not only a wavefunction but probabilistic sum of wavefunctions when we are uncertain as to which one we have.

For example, if we know that a $\ket{0}$ qubit can flip accidentally with a 20% probability then we would say that there is a 80% probability we have the $\ket{0}$ state and a 20% probability that we have a $\ket{1}$ state. This is called an “impure” or “mixed” state. The mixed state isn’t just one wavefunction but instead a distribution over wavefunctions.

## Density Matrix

We represent such a mixed state with something called a density matrix which is a richer representation of quantum states than state vectors. Pure states have very simple density matrices that are written as an outer product of the ket vector representing that state, $\ket{\psi}$, and its complex conjugate $\bra{\psi}$. I.e., the density matrix $\rho_\psi$ is defined as,  $\rho_\psi := \ket{\psi}\bra{\psi}$.

If we want to describe a situation with classical uncertainty between states $\rho_1$ and $\rho_2$, then we can take their weighted sum $(p\rho_1 +(1-p)\rho_2)$, where $p \in [0,1]$ gives the classical probability that the state is $\rho_1$.

## Quantum Gate Noise

There are two basic sources of quantum gate noise:

1. **coherent errors** are those that preserve the purity of the input state, i.e., instead of the intended operation $\ket{\psi} \mapsto U \ket{\psi}$ we carry out a perturbed, but unitary operation $\ket{\psi} \mapsto \tilde{U} \ket{\psi}$, where $\tilde{U} \ne U$.
2. **incoherent errors** are those that do not preserve the purity of the input state, in this case we must actually represent the evolution in terms of density matrices. The state $\rho :=\ket{\psi}\bra{\psi}$ is then mapped as $\rho \mapsto \sum_{j=1}^m K_j \rho K_j ^\dagger$, where the operators $K_1,K_2, ..., K_m$ are called Kraus operators and must obey $\sum_{j=1}^m K_j ^\dagger K_j = \boldsymbol{I}$ to conserve the trace of $\rho$. Maps expressed in this form are called Kraus maps. It can be shown that every physical map on a finite dimensional quantum system can be represented as a Kraus map.

**Cuases of incoherent errors:** When a quantum system (e.g., the qubits on a quantum processor) is not perfectly isolated from its environment it generally co-evolves with the environment's degrees of freedom it couples to. The implication is that while the total time evolution of system and environment as a composite can be assumed to be unitary, the system state by itself might not be.

# Noise Simulation in `qucircuit`

`qucircuit` provides a framework to simulate noise in quantum computers. This allows users to design and evaluate the effects of such noise on quantum algorithms without running them on actual quantum hardware.

`qucircuit` provides two mechanims for adding elements of simulated noise, they can be used individually or together.
1. **Global noise overlay:** a noise profile attached to the circuit which can be setup to add noise automatically at initialization time, and after some or each quantum gate operation, without making any modifications to the circuit's structure.
2. **Applying noise at specific points in the circuit:** by modifying the circuit to add noise operations at specific steps in the quantum circuit.

Refer to the tutorial ipynb notebook for examples of noise modeling [here](https://github.com/atulvarshneya/quantum-computing/blob/master/examples/qckt/noise-sim-tutorial.ipynb)

## Global noise overlay
This mechanism allows the users to create a quantum circuit and then overlay the noise profile to it. This supports noise to be added at 
1. initialization time 
2. to specific qubits when acted upon by any gates,
3. at all gate operations to the qubits acted upon by the gate
4. to specifc qubits at every step of the algorithm
5. after all gates of specific types (e.g., Hadamard gate type, CNOT gate type, etc.).

For this the API `circuit.set_noise_profile(noise_profile)` (poitns #1 to #4 above) and API `circuit.<gate>.set_noise_on_all(noise_channel)` (point #5 above) are to be used. As an example of the latter, `circuit.H.set_noise_on_all(noise_channel)` sets the specified `noise_channel` on Hadamard gate class, so any instance of Hadamard gate in the circuit gets this `noise_channel` applied to its qubits. Note, `set_noise()` on gate instance (see below) overrides noise set on the gate class.

The same effect as using `circuit.set_noise_profile(noise_profile)`, can also be achieved by `circuit = qckt.QCkt(nqubits, nclbits, noise_profile=noise_profile)`.

## Applying noise at specific points in the circuit

`circuit.NOISE(noise_channel, qubits_list)`: this is just like applying a gate, except that instead of a gate operation a noise channel is applied to the specified qubits. The noise channel argument can be either `NoiseChannel` or `NoiseChannelSequence` type.

`circuit.<gate(qubits)>.set_noise(noise_channel)`: this attaches a noise channel to the gate instance and the noise channel acts on the same qubits as the gate, and overrides any noise attached to the gate class. The noise channel should either be a 1-qubit channel, in which case it is 'broadcast' to all the qubits of the gate instance, or the number of qubits of the noise channel must match the number of qubits of the gate it is attached to. 

## Noise channel and noise profile classes

The API uses the following classes to represent the noise channels and the noise profile.

### `NoiseChannel`, `NoiseChannelSequence`
`NoiseChannel` represents one noise channel (a set of operators $K_1, K_2, ..., K_m$ applied as $\sum_{j=1}^m K_j \rho K_j^\dagger$).

The implementation assumes that users might need to apply multiple noise channels as a group in a sequence, the class `NoiseChannelSequence` allows that in an easy way, it represents a sequence of multiple noise channels applied together, one after the other. All API functions that accept an argument of type `NoiseChannel` are designed to also accept that argument to be of type `NoiseChannelSequence`.

### `NoiseChannelApplierSequence` - noise 'applier' specification.
Typically the noise channels are applied along with a gate operation, so they act on the same qubts as the gate, for those purposes it is sufficient to specify the noise as `NoiseChannel` or `NoiseChannelSequence`. However, as part of *noise profile* specification, noise channels can also be applied to specific qubits, this is represented usig the class `NoiseChannelApplierSequence`.

For instance, the noise profile can specify a bit-flip noise on qubits 1 and 2, i.e., to apply this noise after each gate operation involving those qubits.

However, if there is a gate in the circuit that acts on qubits 0 and 1, then after that gate the specified bit-flip noise will be applied to qubit 1  - the qubit common between the gate's target qubits and the noise applier's target qubits. Just to be clear, if the gate acts on qubits other than specified in the applier, that noise in the applier will not be applied.

### `NoiseProfile`
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
4. `noise_chan_allsteps` 
	- noise on specifc qubits at every step of the algorithm 
	- of type `NoiseChannelApplierSequence`

# API Documentation

## Package qckt

### `class QCkt(nqubits, nclbits=None, noise_profile=None, name="QCkt")`
Returns an empty quantum circuit.

noise_profile if not None must be of type `qckt.NoiseProfile`.

### Methods - Gates:
These gate methods instantiate a gate object of the specific type and append it to the quantum circuit. 

For instance,

	import qckt
	circuit = qckt.QCkt(nqubits=2, nclbits=2, name='Example Ckt')
	circuit.H(0)
	circuit.CX(0,1)
	circuit.draw()

would draw the following circuit -

	Example Ckt
	q000 -[H]-[.]-
    	       |  
	q001 -----[X]-
	
	creg =========

#### `CX(control, target)`
Appends a `CNOT` gate to the quantum circuit.

Returns the gate object.

#### `H(qubit)`
Appends a `HADAMARD` gate to the quantum circuit

Returns the gate object.

#### `X(qubit)`
Appends a `NOT` gate to the quantum circuit

Returns the gate object.

#### `Y(qubit)`
Appends a `PAULI-Y` gate to the quantum circuit

Returns the gate object.

#### `Z(qubit)`
Appends a `PAULI-Z` gate to the quantum circuit

Returns the gate object.

#### `T(control1, control2, target)`
Appends a `TOFFOLI` gate to the quantum circuit

Returns the gate object.

#### `M(qubitslist, clbitslist=None)`
Appends `MEASUREMENT` gates for measuring given qubits list into classical bits list

Returns the gate object.

#### `QFT(qubitslist)`
Appends a `QFT` gate across the given qubits list

The drawn circuit depicts multiple `QFT` gates, but it is 1 `QFT` gate acting on those qubits

Returns the gate object.

#### `custom_gate(gatename, op_matrix)`
To add user defined custom gates. 

`gatename` is a string and must follow rules for a legal Python identifier, else will be unuseable; `op_matrix` is the operator matrix in form of `numpy.matrix([...],dtype=complex)`.

The custom gate can then be used as `circuit.gatename(qubits)`. Note that custom gates always accept the target qubits as appropriate number of arguments in the function call, such as `circuit.myCX(0,1)`.

As an example the following circuit -

	import qckt
	import qckt.backend as bknd
	import numpy as np
	ck = qckt.QCkt(3,3)
	ck.custom_gate('myX', np.matrix([[0.0,1.0],[1.0,0.0]],dtype=complex))
	ck.custom_gate('myCX', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,0.0,1.0],[0.0,0.0,1.0,0.0]],dtype=complex))
	ck.H(0)
	ck.myCX(0,1)
	ck.myX(2)
	ck.draw()

creates the following circuit -

	q000 -[H]-[myCX M]---------
			  |      |         
	q001 -----[myCX L]---------
							
	q002 --------------[myX M]-
							
	creg ======================


#### `Border()`
Places a vertical line in the drawing of the quantum circuit. Has effect only in the drawing of the circuit.

Returns the gate object.

#### `Probe(header,probestates)`
This is a debuggig aid. Its execution gets skipped on backends which are actual quantum computers.

`header` is a string that gets prefixed with "PROBE:" and gets printed as a heading to the probe's printout. `probestates` is either `None` or a list of states, if `None`, probe prints amplitude of all the states, else prints the amplitudes of only the specified states.

Returns the gate object.

### Methods - Gate modifier

#### `ifcbit(cbit, value)`
Configures the gate object for the operator to be applied only if the mentioned classical bit, `cbit`, has the mentioned value (0 or 1). `ifcbit` is not supported by `M`, `Border`, and `Probe`.

Exampe usage: apply `X` on `qubit` 4 only if `cbit` 2 has value 0.

	import qckt
	ckt = qckt.QCkt(,4)
	ckt.X(4).ifcbit(2,0)

OR

	import qckt
	ckt = qckt.QCkt(,4)
	xgate = ckt.X(4)
	xgate.ifcbit(2,0)

### Methods - circuit operations:

#### `get_size()`
Returns as a tuple `(nqubits, nclbits)`, the size of quantum and classical registers in the circuit.

#### `realign(newnq, newnc, inpqubits, name=None)`
Creates a potentially wider (more qubits) new circuit from the current circuit with a changed order of the 
qubits. The original circuit is left intact.

All the custom gate definitions from the circuit are copied over to the new circuit.

The argument `name` provides the name of the newly created circuit. If `name` is `None`, then the name of the original circuit is used.

Returns the new circuit

Parameters `newnq` and `newnc` are the sizes of the new (wider or equal sized) circuit
`inpqubits` is a vector that specifies how the old circuit's qubits be replaced in the new circuit.

As an example see the circuits below --

                   current circuit                   new circuit
            q000 ----[H]-[.]----------     q000 --------------------------
                          |                                               
            q001 --------[X]----------     q001 -----------[H]------------
            
            q002 ------------[H]------     q002 --------[X]---------------
                                                         |                
                                           q003 ----[H]-[.]---------------
	     
For this realignment, this vector basically answers the questions `[q002 -> q?, q001 -> q?, q000 -> q?]`
so, the vector should be `[1,2,3]`, and the realign call should be `realign(4,4,[1,2,3])`.

In much simpler terms, consider the current circuit as a large gate, and inpqubits vector basically is 
the way you would use that gate. E.g., `CX` is defined as MSB = control, LSB as target, but if you 
want qubit 2 be control and qubit 4 be target, you would say `CX(2,4)`, i.e., `inpqubits = [2,4]`.

#### `append(othercircuit, name=None)`
Creates a new circuit by appending othercircuit to the current circuit. Both the original circuits are 
left intact.

Returned circuit number of `qubits` match the larger one.  Returned circuit `clbits` match the larger one.

The argument `name` provides the name of the newly created circuit. If `name` is `None`, then the name of the original circuit is used.

All the custom gate definitions from both the circuits are copied over to the new circuit.

Returns the updated new circuit.

#### `draw(show_noise=True)`
Draws a text drawing of the circuit. The argument `show_noise` selects if the noise elements are drawn or hidden.

#### `list()`
prints out the sequence of gates in the circuit.

In the current release (Rel 2.0) `list()` does not support displaying the noise elemetns of the circuit.

#### `get_gates_list()`
returns list of all gates available in this circuit. Note any custom gates are included in the list.

### Methods - noise API

#### `set_noise_profile(noise_profile)`

attaches a noise profile to the circuit.

Example usage:

	import qckt
	import qckt.noisemodel as ns
	circuit = qckt.QCkt(2,2)
	circuit.H(0)
	circuit.CX(0,1)

	noise_profile = ns.NoiseProfile(
		noise_chan_allgates=ns.bit_flip(probability=0.1),
		)
	circuit.set_noise_profile(noise_profile)
	draw()

which has output as:

	q000 -[H]-[H:BF(0.10)]-[.]-[CX:BF(0.10)]-
							|                
	q001 ------------------[X]-[CX:BF(0.10)]-
											
	creg ====================================

#### `<gate_class>.set_noise_on_all(noise_chan)`

Specifies `noise_chan` to all instances of the gale class.

Example usage:

	import qckt
	import qckt.noisemodel as ns
	circuit = qckt.QCkt(3,3)
	circuit.H(0)
	circuit.H(2)
	circuit.CX(0,1)

	circuit.H.set_noise_on_all(ns.phase_flip(probability=0.05))
	circuit.draw()

which has the output:

	q000 -[H]-[H:PF(0.05)]------------------[.]-
											 |  
	q001 -----------------------------------[X]-
												
	q002 ------------------[H]-[H:PF(0.05)]-----
												
	creg =======================================

#### `<gate>(<gate-arguments).set_noise(noise_channel)`

attaches `noise_channel` to the gate invokation.

Example usage:

	import qckt
	import qckt.noisemodel as ns
	circuit = qckt.QCkt(2,2)
	circuit.H(0)
	circuit.CX(0,1).set_noise(ns.bit_flip(0.1))
	circuit.draw()

which has output:

	q000 -[H]-[.]-[CX:BF(0.10)]-
			   |                
	q001 -----[X]-[CX:BF(0.10)]-
								
	creg =======================

#### NOISE(noise_channel, qubits_list)

Incorporates a noise step in the circuit.

Example usage:

	import qckt
	import qckt.noisemodel as ns
	circuit = qckt.QCkt(2,2)
	circuit.H(0)
	circuit.CX(0,1)
	circuit.NOISE(ns.phase_flip(0.1), [0,1])
	circuit.draw()

which has outout as:

	q000 -[H]-[.]-[NS:PF(0.10)]-
			   |                
	q001 -----[X]-[NS:PF(0.10)]-
								
	creg =======================
 
### `class Job`
Packages the job to be executed on a backend engine.

`Job` object converts the circuit to an array of implementation neutral, fully-specified operations (gates, 
measurement, probes (for simulator backends), and all noise elements).

Once executed, the backend engine populates the results in the job object.

The constructor takes the following arguments -
* circuit - a QCkt() object
* initstate - default value `None`. The initial state the quantum computer to be initialized with
* prepqubits - default value `None`. Another way to specify the initial state, by providing the state vector
* qtrace - default value `False`. If using a debugging version of the backend engine, specifies if at each step the state of the computation be printed out.
* shots - default value 1. The number of times the circuit should be run. The measured values are stored for each run. For debugging version backend engine the number of shots is set to 1.

#### Methods

#### `job.get_creg()`
returns an array of `Cregister` objects from all runs/shots.

#### `job.get_counts()`
returns the frequencies of different `Cregister` values in the results.

#### `job.plot_counts()`
plots the counts in a visual form using text characters.

If running in Jupyter notebook, plots using `matplotlib`.

#### `job.get_svec()`
only useful for state-vector based simulator backends, returns the state-vector at the end of the execution. `shots` must be only 1. In density matrix based simulator backends, the trace of the density matrix is returned (effectively square of the amplitudes of the state vector).


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

#### `get_runstats()`

Returns the run stats as a dictoinary object -

	{
		'QSteps': qsteps, 
		'OpCounts': op_counts_dict, 
		'OpTimes': op_times_dict
	}

	op_counts_dict is a dictionary with key as the gate name, and value as the total count of times it was invoked in the run.
	op_times_dict is a dictionary with key as the gate name, and value as the total time the simulator took running all the gate's invokations.

#### `print_runstats()`
Prints a report of the run stats.

Example usage:

	import qckt
	import qckt.backend as bknd

	ckt = qckt.QCkt(2,2)
	ckt.H(0)
	ckt.CX(0,1)

	job = qckt.Job(circuit=ckt)
	bk = bknd.DMQeng()
	bk.runjob(job=job)

	job.print_runstats()

which gives output as

	Total Ops  :     2      operations
	Total Time :     0.0036 sec
	Per Operation:
		H           0.0030 sec     1 times 0.0030 avg
		CX          0.0006 sec     1 times 0.0006 avg


# Package `qckt.noisemodel`

## class NoiseChannel

Class to represent a noise channel.

Example:

	p = 0.1
	noise_chan = ns.NoiseChannel(
		name='myChan',
		nqubits=1,
		noise_chan=[(kraus_op1,p),(kraus_op2,(1-p))]
		)

The objects of this class are iterable, and returns a tuple `(kraus_op, probability)` at each iteration.

## class NoiseChannelSequence

Class to represent a sequence of noise channels.

Constructor takes any number of noise channels - 

	chan_seq = NoiseChannelSequence(chan1,chan2,chan3)

The objects of this class are iterable, and returns a noise channel in the sequence at each iteration.

### Methods

#### `add_noise_chan(noise_channel)`

Appends a noise channel to the sequence.

#### `add_noise_chan_sequence(noise_channel_sequence)`

Appends a channel sequence to the sequence.

## class NoiseChannelApplierSequence

Class to represent noise channel 'applier'. The term applier refers to a set of tuples `(noise_channel,qubits_list)`.

Constructor takes a `NoiseChannel` or `NoiseChannelSequence` object as the first argument, and a list of qubits as the second arguments.

The objects of this class are iterable, and returns a tuple `(noise_channel, qubits_list)` in the applier at each iteration.

### Methods

#### `add(noise_channel, qubits_sequence)`

Takes the same arguments as the constructor, and adds the tuples `(noise_channel,qubits_list)` to the sequence.

#### `extend(noise_channel_applier_sequence)`

Appends the tuples from the applier argument to the sequence in the object.

## class NoiseProfile

Class to represent the noise profile. Has the following fields,
* `noise_chan_init` which contains either `None` (default), or contains a `NoiseChannel`, or `NoiseChannelSeuence` object.
* `noise_chan_allgates` which contains either `None` (default), or contains a `NoiseChannel`, or `NoiseChannelSeuence` object.
* `noise_chan_qubits` which contains either `None` (default), or contains a `NoiseChannelApplierSequence` object.
* `noise_chan_allsteps` which contains either `None` (default), or contains a `NoiseChannelApplierSequence` object.

Constructor signature -

	`NoiseProfile(
		noise_chan_init=None,
		noise_chan_allgates=None,
		noise_chan_qubits=None,
		noise_chan_allsteps
		)`

# Package `qckt.gatesutils`

#### `stretched_opmatrix(nqbits, oper, qbit_list)`
Converts the quantum gate's operator matrix into a matrix for a system with larger number of qubits. 
The qubits on which the gate operates are kept as the highest order qubits, the additional qubits are 
left unchanged by the *stretched* operator.

#### `combine_opmatrices_par(op_list)`
Combines two or more operator matrices into one when they act on separate set of qubits simultaneously.

Returns the generated operator matrix.

#### `combine_opmatrices_seq(op_list)`
Combines two or more operator matrices into one when they act on the same set of qubits sequentially.

Returns the generated operator matrix.

#### `isunitary(mat)`
Checks if the given operator matrix is unitary or not.

Returns a boolean (`True`/`False`).

#### `opmat_dagger(opMat)`
Returns the conjugate transpose (dagger) of a given operator matrix.

#### `CTL(opMatrix)`
Utility function to add a control bit to an operator matrix (`opMatrix`).

Returns the generated operator matrix.

# Package qckt.backend (Backend framework)

## Backend Services Registry
This is an API for accessing the registry of Quantum Computing Services registered at your installation's configuration. `listSvc()` returns a list of tuples (name, description) of all services available (i.e. registered in the installation's configuration) `getSvc(svcName)` returns handle to the named backend service.

Example usage:

	import qckt.backend as bknd
	reg = bknd.Registry()
	svcTuples = reg.listSvc()
	svc = reg.getSvc("QSystems")

## Backend Service
Backend service implments the methods to connect with the quantum computing service (through authentication/authorization as required). The service provides methods to discover backend engines under that service, and get the handles to them to run the quantum computing circuits/programs.

`listInstances()` returns a list of tuples (name, description) of all instances (quamtum computers) available at this service.

`getInstance(name)` returns an object representation of the named instance (quantum computer).

Example usage: Going through the `Registry`

	import qckt.backend as bknd
	reg = bknd.Registry()
	svcTuples = reg.listSvc()
	svc = reg.getSvc("QSystems")
	engine_list = svc.listInstances()
	engine = svc.getInstance("qsim-eng")

Example usage: Directly accessing the engines from `QSystems` service

	import qckt.backend as bknd
	debugging_engine = bknd.Qdeb() # same as svc.getInstance("qsim-eng")
	engine = bknd.Qeng() # same as svc.getInstance("qsim-deb")

## Backend engines

Current release of `qucircuit` uses the engines from `qusimulator` as backends.

`qusimulator` provides two kinds of engines - 
* state-vector based engines, and 
* density-matrix based engines

For noise simulation the density-matrix engines should be used - `dmqsim-eng` and its debugging version `dmqsim-deb`. The state-vector engines `qsim-end` and `qsim-deb` run the circuits ignoring all noise aspects in the circuit. From functionality purposes, the engines are 'drop-in' replacements for each other.

The debugging versions of engines provide the capability of tracing the execution of the circuit by displaying the state-vector/density matrix and the classical bits register at each step. This tracing is enabled by setting the argument `qtrace=True` in the `Job` object.

### Backend Engine Adaptors

The adaptor for the backend needs to interpret the operations sequence in the `qckt` representation.
At the end of the job execution (all the shots), the backend adaptor populates the results in the `job` object, as mentioned above.

`runjob(job)` - this is the only function implemented by the backend adaptor. It runs the given `job` on the backend execution engine. It returns the backend adaptor object itself.

Example usage: Directly accessing the QSystems engines

	import qckt
	import qckt.backend as bknd
	bk_engine = bknd.Qeng() # same as svc.getInstance("qsim-eng")
	job = qckt.Job(somecircuit, initstate=somestate, shots=100)
	bk_engine.runjob(job)

## Backend results classes

### `class Cregister`
An object of this class is returned by `job.get_creg()`, and holds the classical register value got from the measurement operations. It provides method to convert that to a pretty printable string, e.g., in `str(cregister)`, `print(cregister)`.
The classical bits array can be accessed through the `.value` field and its integer value through `.intvalue` field of the returned object.

This class is available in `qckt.backend`.

### `class StateVector`
An object of this class is returned by `job.get_svec()`, and holds the *statevector* value from the simulator backend engine. Note that state is available only when you run on a simulator, not on an actual QC hardware. In case of DM simulator, the diagonal of the density operator is returned.

It provides methods to convert that to pretty printable string, e.g., in `str(statevector)`, `print(statevector)`.
The *statevector* array can be accessed through the `.value` field of the object
The returned object also supports a method `StateVector.verbose(boolean)`, which affects the string conversion such that it includes all states even those with an amplitude of 0. `StateVector.verbose(boolean)` returns the same state-vector object.

This class is available in `qckt.backend`.

