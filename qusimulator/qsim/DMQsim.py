#!/usr/bin/python3

# This file is part of the QSIM project covered under GPL v3 license.
# See the full license in the file LICENSE
# Author: Atul Varshneya

from qsim.qSimException import QSimError
import qsim.noisemodel as nmdl
import numpy as np
import random as rnd
from copy import deepcopy
import time
import sys

## IMPORTANT: The qubit/clbit ordering convention is -- [MSB, ..., LSB]. Yes, :-), [0] is MSB.
##            NOTE: when refering to bits by position numbers, MSB would be 7, in an 8-qubit machine
##            So, CNOT 3,0 in an 8-qubit machine, woudld act on [ -, -, -, -, C, -, -, T], C=control, T = target
##            BUT, the state vector ordering is [0000, ...., 1111]. Good that it does not impact the user.
## Sorry, for this confusion, but too much effort to change now.

class DMQSimulator:

	def __init__(self,
			nqbits,
			ncbits=None,
			initstate=None,
			prepqubits=None,
			noise_profile=None,
			qtrace=False,
			qzeros=False,
			verbose=False,
			validation=False,
			visualize=False):
		# record input variables for reset
		self.nqbits = nqbits
		self.ncbits = ncbits
		if self.ncbits is None:
			self.ncbits = nqbits
		self.initstate = initstate
		self.prepqubits = prepqubits
		self.sys_state = None
		self.traceINP = qtrace
		self.disp_zerosINP = qzeros
		self.verbose = verbose
		self.validation = validation
		self.visualize = visualize

		# noise profile
		self.noise_profile = noise_profile
		if self.noise_profile is not None:
			noise_profile_keys = ['noise_chan_init', 'noise_chan_allgates', 'noise_chan_qubits']
			for k in self.noise_profile.keys():
				if k not in noise_profile_keys:
					raise QSimError(f'ERROR: incorrect key name {k} in noise_profile')

			noise_chan_allgates = self.noise_profile.get('noise_chan_allgates', None)
			if noise_chan_allgates is not None:
				if type(noise_chan_allgates) is nmdl.qNoiseChannel:
					self.noise_profile['noise_chan_allgates'] = nmdl.qNoiseChannelSequence(noise_chan_allgates)
				elif type(noise_chan_allgates) is nmdl.qNoiseChannelSequence:
					pass
				else:
					raise QSimError(f'ERROR: noise_chan_allgates must be an object of class qNoiseChannelSequence')
			# self.noise_profilel['noise_chan_allgates'] used in qgate() to apply this noise to qubits of every gates

			noise_chan_init = self.noise_profile.get('noise_chan_init', None)
			if noise_chan_init is not None:
				if type(noise_chan_init) is nmdl.qNoiseChannel:
					self.noise_profile['noise_chan_init'] = nmdl.qNoiseChannelSequence(noise_chan_init)
				elif type(noise_chan_init) is nmdl.qNoiseChannelSequence:
					pass
				else:
					raise QSimError(f'ERROR: noise_chan_init must be an object of class qNoiseChannelSequence')
				# check that noise_chan_init has only 1-qubit qNoiseChannel objects
				noise_chan_init = self.noise_profile['noise_chan_init']
				for chan in noise_chan_init:
					if chan.nqubits != 1:
						raise QSimError(f'ERROR: noise_chan_init must use 1-qubit noise channel')
			# the self.noise_profile['noise_chan_init'] noise is applied in __initialize_sim() after creating self.sys_state

			noise_chan_qubits = self.noise_profile.get('noise_chan_qubits',None)
			if noise_chan_qubits is not None:
				if type(noise_chan_qubits) is not nmdl.qNoiseChannelApplierSequense:
					raise QSimError(f'ERROR: noise_chan_qubits must be an object of class qNoiseChannelApplierSequense')
			# this is used in qgate() to apply this noise to qubits of every gates where the qubits are used


		# runstats
		self.qsteps = 0
		self.op_times = {}
		self.op_counts = {}

		# Useful constants
		self.pi = np.pi
		self.errprec = 6 # number of digits after decimal
		self.maxerr = 10**(-self.errprec)
		self.probprec = 6 # number of digits after decimal
		self.maxproberr = 10**(-self.probprec)

		self.__initialize_sim()

	def qreset(self):
		print(f'WARNING: qreset() is deprecated. Reinstantiate the DMQsimulator object instead.', file=sys.stderr)
		self.__initialize_sim()
	def __initialize_sim(self):
		# Reset the runtime Variables, in case qtraceON(), qzerosON() have changed them.
		self.trace = self.traceINP
		self.disp_zeros = self.disp_zerosINP

		# clear the runstats
		self.qsteps = 0
		self.op_times = {}
		self.op_counts = {}

		# Clear the classical bits register
		self.cregister = [0]*self.ncbits

		# Initial State
		if not self.initstate is None:
			# check if the state is np.matrix type
			if not type(self.initstate) is np.matrixlib.defmatrix.matrix:
				errmsg = "User Error. Wrong type. Initstate must be a numpy.matrix."
				raise QSimError(errmsg)
			# check if the size of the passed state is 2**nqbits
			(rows,cols) = self.initstate.shape
			if rows != 2**self.nqbits or cols != 1:
				errmsg = "User Error. wrong dimensions. Initstate shape must be (2^nqbits,1)."
				raise QSimError(errmsg)
			# check if normalized
			p = 0
			for i in range(2**self.nqbits):
				p += np.absolute(self.initstate[i].item(0))**2
			if np.absolute(p-1.0) > self.maxerr:
				errmsg = "User Error. Initial state not normalized."
				raise QSimError(errmsg)
			self.sys_state = deepcopy(self.initstate)
			# Now convert the state vector to density matrix
			self.sys_state = np.matrix(np.outer(self.sys_state, np.conjugate(self.sys_state)))
		elif not self.prepqubits is None:
			if len(self.prepqubits) != self.nqbits:
				errmsg = "User Error. wrong dimensions. prepqubits has incorrect number of qbits."
				raise QSimError(errmsg)
			pqbit = np.transpose(np.matrix(self.prepqubits[self.nqbits-1],dtype=complex))
			prepstate = pqbit
			for i in reversed(range(self.nqbits-1)):
				pqbit = np.transpose(np.matrix(self.prepqubits[i],dtype=complex))
				prepstate = np.kron(pqbit,prepstate)
			p = 0
			for i in range(len(prepstate)):
				p += np.absolute(prepstate[i].item(0))**2
			prepstate = prepstate/np.sqrt(p)
			self.sys_state = prepstate
			# Now convert the state vector to density matrix
			self.sys_state = np.matrix(np.outer(self.sys_state, np.conjugate(self.sys_state)))
		else:
			# initialize the qbits to |0>
			qbit = [None]*self.nqbits
			for i in range(self.nqbits):
				qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
			# Now create the state as a tensor product of the qbits (MSB to the left)
			self.sys_state = qbit[self.nqbits-1]
			for i in reversed(range(self.nqbits-1)):
				self.sys_state = np.kron(qbit[i],self.sys_state)
			# Now convert the state vector to density matrix
			self.sys_state = np.matrix(np.outer(self.sys_state, np.conjugate(self.sys_state)))

		# Now apply noise_chan_init
		noise_tag = ''
		if self.noise_profile is not None:
			noise_chan_init = self.noise_profile.get('noise_chan_init',None)
			if noise_chan_init is not None:
				all_qbits = list(range(self.nqbits))
				noise_chan_init_applier = nmdl.qNoiseChannelApplierSequense(noise_chan=noise_chan_init, qubit_list=all_qbits)  # [[chan,all_qbits] for chan in self.noise_chan_init]
				self.__apply_noise(noise_chan_init_applier)
				noise_tag = f' NOISE:[{noise_chan_init_applier.name}]'

		if self.trace:
			self.qreport(header="Initial State"+noise_tag)


	# following are the structures explained wrt the noise in quantum operations
	# 
	# quantum operation:
	#     qop = [name, opmatrix]
	# 
	# qNoiseChannel: this is returned by the functions in noisemodel/noiseOperators.py. 
	# Users can construct custom noise_channels and use them.
	#     opprob_set = [(qop, prob), (qop,prob), ...]
	#     name = 'myChan'
	#     nqubits = nq  # number of qubits the noise_chan acts on
	#     noise_chan = qsim.noisemodel.qNoiseChannel(name=name, operator_prob_set=opprob_set, nqubits=nq)
	#
	# noise channel sequence: this structure is provided as arguments to qnoise() and qgate() functions,
	# as well as QC constructor as part of noise_profile parameters noise_chan_init and noise_chan_allgates
	#      noise_chan_seq = qsim.noisemodel.qNoiseChannelSequence(noise_chan1, noise_chan1, ...)
	# 
	# noise chan seq applier: this is used in QC constructor noise_profile to specify noise for specific qubits, noise_chan_qubits.
	#      noise_chan_applier_seq = qsim.noisemodel.qNoiseChannelApplierSequence()
	#      noise_chan_applier_seq.add(noise_chan_seq1, qubit_list1)
	#      noise_chan_applier_seq.add(noise_chan_seq2, qubit_list2)
	# 
	# noise profile: 
	#      noise_profile = {
	# 			'noise_chan_init': noise_chan_seq,           # e.g., [bit_flip(0.1), phase_flip(0.1)]
	# 			'noise_chan_qubits': noise_chan_applier_seq  # e.g., [(depolarizing(0.1),[0,1]), ()]
	# 			'noise_chan_allgates': noise_chan_seq,       # e.g., [bit_flip(0.1), amplitude_damping(0.15), phase_damping(0.1)]
	# 	}
	# 
	# 
	# 
	# The rationale is as following -
	# 1. noise is expected to be applied as a sequence of noise channels, hence that represents 
	#    a unit of noise application
	# 2. qnoise() therefore takes noise_chan_seq as the input, along with the qubits list to which 
	#    it is applied.
	# 3. qgate() also takes noise arguments exactly the same as qnoise.
	#    qgate() combines the noise_chan_applier_seq specified as a default for certain qubits, 
	#    noise_chan_seq for all gates, and the specific noise_chan_seq specified for this qgate invokation,
	#    and constructs the consolidated noise_chan_applier_seq
	#    for the combined noise
	# 4. __apply_noise() takes noise_chan_applier_seq as the argument. The calling function must 
	#    construct this object.
	#    NOTE: noise_chan_seq_applier can take a hetrogeneous mix of 1-qubit and 2-qubit noise channels
	#    as long as they are matched with the valid number of qubits
	#    NOTE: (TODO) If the noise_chan_seq_applier includes a 2-qubit noise channel, the corresponding
	#    qubit list argument must be exactly 2 qubits, else an exception will be raised

	def qnoise(self, noise_chan, qbit_list, qtrace=False):
		# TODO check for 1-qubit noise chan => variable num of qubits allowed.
		# If 2-qubit noise chan, then only 2 qubits allowed

		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits)
		if not self.__valid_bit_list(qbit_list,self.nqbits):
			errmsg = f"Error: the list of qubits {qbit_list} is not valid."
			raise QSimError(errmsg)

		# check noie_chan argument
		if type(noise_chan) is nmdl.qNoiseChannel:
			noise_chan_seq = nmdl.qNoiseChannelSequence(noise_chan)
		elif type(noise_chan) is nmdl.qNoiseChannelSequence:
			noise_chan_seq = noise_chan
		else:
			raise QSimError('ERROR: qNoiseChannelSequence or qNoiseChannel object expected.')

		noise_chan_applier_sequence = nmdl.qNoiseChannelApplierSequense(noise_chan=noise_chan_seq, qubit_list=qbit_list)

		self.__apply_noise(noise_chan_applier_sequence=noise_chan_applier_sequence)
		# noise channels are trace preserving, so check that here
		assert(abs(np.trace(self.sys_state) - 1.0) < self.maxerr)

		# get the name of the noise
		noise_name = noise_chan_applier_sequence.name

		if qtrace or self.trace:
			opname = f'NOISE:[{noise_name}]'
			opargs = str(qbit_list)
			hdr = opname
			self.qreport(header=hdr)


	# noise_chan_applier_seuence = (noise_chan,qbit_list), (noise_chan,qbit_list), ...
	def __apply_noise(self, noise_chan_applier_sequence):
		for noise_chan_applier in noise_chan_applier_sequence:
			noise_channel, qbit_list = noise_chan_applier
			# apply the noise on the specified qubits
			# CHECK the channel dimension, whether 1-qubit or 2-qubits channel
			# chan = noise_channel.operator_prob_set
			if noise_channel.nqubits == 1:
				for qbit in qbit_list:
					# calculate the noise to be added for this qubit
					state_noise_cumulative = np.matrix(np.zeros((2**self.nqbits, 2**self.nqbits)), dtype=complex)
					for op,prob in noise_channel:
						a_op = self.__stretched_mat(op,[qbit])
						state_noise_component = prob * (a_op * self.sys_state * np.transpose(np.conjugate(a_op)))
						state_noise_cumulative = state_noise_cumulative + state_noise_component
					# update sys state
					self.sys_state = state_noise_cumulative
					# self.qreport(header=f'state after noise added to qubit {qbit}',state=self.sys_state)
			else:
				if len(qbit_list) != noise_channel.nqubits:
					raise QSimError(f'ERROR: number of qubits in argument for {noise_channel.name} is invalid.')
				state_noise_cumulative = np.matrix(np.zeros((2**self.nqbits, 2**self.nqbits)), dtype=complex)
				for op,prob in noise_channel:
					a_op = self.__stretched_mat(op,qbit_list)
					state_noise_component = prob * (a_op * self.sys_state * np.transpose(np.conjugate(a_op)))
					state_noise_cumulative = state_noise_cumulative + state_noise_component
				# update sys state
				self.sys_state = state_noise_cumulative
				# self.qreport(header=f'state after noise added',state=self.sys_state)


	def qgate(self, oper, qbit_list, ifcbit=None, noise_chan=None, qtrace=False):  # ifcbit is encoded as tuple (cbit, ifvalue)
		# runstats - sim cpu time
		st = time.process_time()

		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits
		if not self.__valid_bit_list(qbit_list,self.nqbits):
			errmsg = "Error: the list of qubits is not valid."
			raise QSimError(errmsg)
		if self.validation:
			if not self.qisunitary(oper):
				errmsg = "Error: Operator {:s} is not Unitary".format(oper[0])
				raise QSimError(errmsg)

		# Put together noise applier:
		noise_chan_applier_sequence_overall = nmdl.consolidate_gate_noise(self.noise_profile, noise_chan, qbit_list)
		# get the name of the noise
		noise_name = noise_chan_applier_sequence_overall.name

		cbit_cond = True
		if not ifcbit is None:
			# check the validity of the ifcbit[0] (reapeated cbits, all cbits within self.ncbits)
			if not self.__valid_bit_list([ifcbit[0]],self.ncbits):
				errmsg = "Error: the ifcbit[0] value is not valid."
				raise QSimError(errmsg)
			if ifcbit[1] != 0 and ifcbit[1] != 1:
				errmsg = "Error: the ifcbit[1] value is not valid."
				raise QSimError(errmsg)
			cbit_cond = ( self.cregister[self.ncbits-1-ifcbit[0]] == ifcbit[1] )

		# perform the gate operation if cbits condition is satisfied
		if cbit_cond:
			a_op = self.__stretched_mat(oper,qbit_list)
			self.sys_state = a_op * self.sys_state * np.transpose(np.conjugate(a_op))

			# and, apply noise
			self.__apply_noise(noise_chan_applier_sequence=noise_chan_applier_sequence_overall)

		# overall gate application, including noise operators, is trace preserving, so check that here
		assert(abs(np.trace(self.sys_state) - 1.0) < self.maxerr)

		if qtrace or self.trace:
			opname = oper[0]
			opargs = str(qbit_list)
			noise_part = '' if noise_name == '' else f' NOISE:[{noise_name}]'
			cond_cbit_arg = '' if ifcbit is None else ' if Cbit'+str(ifcbit[0])+'='+str(ifcbit[1])
			hdr = opname + " Qubit" + opargs + noise_part + cond_cbit_arg
			self.qreport(header=hdr)

		#update runstats
		et = time.process_time()
		self.op_times[oper[0]] = self.op_times.get(oper[0], 0.0) + (et-st)
		self.op_counts[oper[0]] = self.op_counts.get(oper[0], 0) + 1
		self.qsteps += 1

	def qsnapshot(self):
		return self.cregister, np.squeeze(np.asarray(self.sys_state)), {'QSteps':self.qsteps, 'OpCounts':self.op_counts, 'OpTimes':self.op_times}

	def qmeasure(self, qbit_list, cbit_list=None, qtrace=False):
		# runstats - sim cpu time
		st = time.process_time()
		oper = ["MEASURE"] # use this to lookup name as in a qgate call

		# check the validity of the qbit_list (reapeated qbits, all qbits within self.nqbits)
		if not self.__valid_bit_list(qbit_list,self.nqbits):
			errmsg = "Error: the list of qubits is not valid."
			raise QSimError(errmsg)

		if cbit_list is None:
			cbit_list = qbit_list
		# check the validity of the cbit_list (reapeated cbits, all cbits within self.ncbits)
		if not self.__valid_bit_list(cbit_list,self.ncbits):
			errmsg = "Error: the list of cbits is not valid."
			raise QSimError(errmsg)
		# check if equal number of qbits and cbits are passed
		if len(qbit_list) != len(cbit_list):
			errmsg = "Error: number of qbits and cbits passed are unequal."
			raise QSimError(errmsg)

		# align the qbits-to-measure to the MSB
		qbit_reorder = self.__qbit_realign_list(qbit_list)
		(rmat,rrmat) = self.__rmat_rrmat(qbit_reorder)
		# we have density matrix, so alignment for rows as well as columns
		self.sys_state = rmat * self.sys_state
		self.sys_state = np.transpose(rmat * np.transpose(self.sys_state))

		list_len = len(qbit_list)
		qbitmask = 0
		for b in range(list_len):
			qbitmask |= 0x1 << (self.nqbits-b-1)
		shift_bits = self.nqbits - list_len

		# construct a M matrix for each possible value of qubits being measured.
		# E.g., if qbits 0,1 are being measured, create M00, M01, M02, M03.
		n_Mmats = 2**len(qbit_list)
		Mmats = [None] * n_Mmats
		prob = [0.0] * n_Mmats # later we will store the probabilities of each M observable
		for i in range(n_Mmats):
			Mmats[i] = np.matrix(np.zeros(self.sys_state.shape), dtype=complex)
		for i in range(2 ** self.nqbits):
			Mmat_idx = (i & qbitmask) >> shift_bits # Hmmm, could have kept the opposite bit order; too late now!!
			Mmats[Mmat_idx][i,i] = 1.0
		for i in range(n_Mmats):
			eta = Mmats[i] * self.sys_state * Mmats[i]
			prob[i] = np.trace(eta)

		# OK, now see which one should be selected
		toss = rnd.random()
		sel = len(prob) - 1 # to default if all the probs add up just short of 1, and toss == 1
		prob_val = prob[sel]
		cumprob = 0
		for i in range(len(prob)):
			if toss > cumprob and toss <= (cumprob + prob[i]):
				sel = i
			cumprob += prob[i]
		prob_val = np.absolute(prob[sel])
		meas_val = []
		for i in reversed(range(list_len)):
			if (sel & (0x1<<i)) == 0:
				meas_val.append(0)
			else:
				meas_val.append(1)

		# now, collapse to the selected state density matrix
		eta = Mmats[sel] * self.sys_state * Mmats[sel]
		self.sys_state = eta/prob_val

		# align the qbits back to original
		self.sys_state = np.transpose(rrmat * np.transpose(self.sys_state))
		self.sys_state = rrmat * self.sys_state

		# finally update classical bits register with the measurement
		for i in range(len(cbit_list)):
			self.cregister[self.ncbits - cbit_list[i]-1] = meas_val[i]

		if qtrace or self.trace:
			hdr = "MEASURED "+"Qubit" + str(qbit_list) + " = " + str(meas_val) + " with probability = " + str(round(prob_val,self.probprec-1)) 
			self.qreport(header=hdr)

		#update runstats
		et = time.process_time()
		self.op_times[oper[0]] = self.op_times.get(oper[0], 0.0) + (et-st)
		self.op_counts[oper[0]] = self.op_counts.get(oper[0], 0) + 1
		self.qsteps += 1

		return meas_val


	def qreport(self, header="State", state=None, probestates=None, visualize=False):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		if state is None:
			state = self.sys_state
		st_diag = np.diagonal(state)
		if probestates is not None:
			header = header + " - Probestates: "+str(probestates)
		print(header)

		verbose = self.verbose
		if self.disp_zeros:
			verbose = False # cannot print columns of sys density matrix if also displaying zeros
		# identify rows and columns to print that are non-zero or disp_zeros is set
		(nrows,ncols) = state.shape
		pr_row = [False]*nrows
		pr_col = [False]*nrows
		for i in range(nrows):
			for j in range(ncols):
				if np.absolute(state[i,j]) > self.maxerr or self.disp_zeros:
					pr_row[i] = True
					pr_col[j] = True

		for i,row in enumerate(np.array(state)):
			if (probestates is None and pr_row[i]) or (probestates is not None and i in probestates):
				print(('{:0'+str(self.nqbits)+'b}    ').format(i), end='')
				if verbose:
					for j,v in enumerate(row):
						if (probestates is None and pr_col[j]) or (probestates is not None and j in probestates):
							print(f'{v:.2f} ', end='')
				else:
					print('...', end='')
				print(f' | {st_diag[i]:.4f}')
		# print(f'Trace : ----  {np.trace(state):.4f}')
		purity = np.trace(state * state).real
		print(f'Mixed State Purity: {purity:.4f}')
		print("CREGISTER: ", end="")
		for i in range(self.ncbits): # cregister[0] is MSB
			print("{0:01b}".format(self.cregister[i]),end="")
		print()
		print()

	def qsize(self):
		return self.nqbits

	def qtraceON(self, val):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		self.trace = val

	def qzerosON(self, val):
		# This is only a simulator function for debugging. it CANNOT be done on a real Quantum Computer.
		self.disp_zeros = val


	####################################################################################################
	## Utility functions ###############################################################################
	####################################################################################################

	def __valid_bit_list(self,bit_list,nbits):
		if len(bit_list) > nbits:
			return False
		for i in bit_list:
			if i >= nbits:
				return False
			if bit_list.count(i) != 1:
				return False
		return True

	def __shuffled_count(self, bitorder):
		sz = self.nqbits
		shuffled = []
		for i in range(2**sz):
			shfval = 0
			for b in range(sz):
				dstbit = bitorder[sz-b-1]
				shfval += (((i >> b) & 0x1) << dstbit)
			shuffled.append(shfval)
		return shuffled

	def __rmat_rrmat(self, qbit_reorder):
		# this is the counting with the given bit ordering
		rr = self.__shuffled_count(qbit_reorder)
		## create the rmat and rrmat
		imat = np.matrix(np.eye(2**self.nqbits))
		rmat = np.matrix(np.eye(2**self.nqbits))
		rrmat = np.matrix(np.eye(2**self.nqbits))
		for i in range(2**self.nqbits):
			s = rr[i]
			rmat[i] = imat[s]
			rrmat[s] = imat[i]
		return (rmat, rrmat)

	def __qbit_realign_list(self, qbit_list):
		reord_list = deepcopy(qbit_list)
		for i in reversed(range(self.nqbits)): # reversed to maintain significance order of the other qbits; poetic correctness :-)
			if i not in reord_list:
				reord_list.append(i)
		return reord_list

	## __aligned_op() and __stretched_mat() use two concepts core to
	## the working of this simulator.
	##
	## methods __qbit_realign_list(), __rmat_rrmat(), and __shuffled_count() are used
	## for the alignment of the operators as described below --
	##
	## Lets consider a 2-bit gate, e.g., CNOT gate, C, which, say, is defined
	## to take bit 1 as the control bit, and bit 0 as the target bit --
	##
	##         +---+
	## |b1> ---|-+-|------
	##         | | |
	## |b0> ---|-O-|------
	##         +---+
	##
	## Lets see how we apply this 2-qubit gate to some specifc bits of a 4 qubit system,
	## say, control qubit 1, and target qubit 3.
	## We first 'stretch' this to the full 4 qubits U = np.kron(C, np.eye(4)). See below 
	## the description of __stretched_mat().
	##         +---+
	## |b3> ---|-+-|------
	##         | | |
	## |b2> ---|-O-|------
	##         |   |
	## |b1> ---|---|------
	##         |   |
	## |b0> ---|---|------
	##         +---+
	##           U
	## Note, U operator is a 2**nqbits x 2**nqbits matrix, 16x16 in this example case.
	## And note, that this will apply the operation to the qubits 3 (control) and 2 (target) i.e., 
	## most-significant qubits, and leave the other qubits unchanged.
	##
	## Remember, operators act on a state vector to compute the resulting state 
	## vector, that is why the operator is 2**nqbits x 2**nqbits in size
	##
	## Next, we apply an operator, r, a 2**nqbits x 2**nqbits matrix, on the state 
	## to reorder (realign) it such that the state vector is ordered counting with qubit 1 
	## at qubit 3 position, and qubit 3 at qubit 2 position. 
	## Next, apply U. Finally, apply an operator, rr, to undo the reordering done by 
	## the operator r.
	## So logically, the operators circuit diagram looks like -
	##         +---+  +---+  +---+
	## |b3> ---|3 1|--|-+-|--|1 3|----
	##         |   |  | | |  |   |
	## |b2> ---|2 3|--|-O-|--|3 2|----
	##         |   |  |   |  |   |
	## |b1> ---|1 2|--|---|--|2 1|----
	##         |   |  |   |  |   |
	## |b0> ---|0 0|--|---|--|0 0|----
	##         +---+  +---+  +---+
	##           r      U      rr
	## 
	## Now, if we multiple these three operators as a_op = (rr x U x r) then the resulting 
	## operator, calling it a_op, basically is the one that applies C on qubits 1 and 3 as intended.

	def __aligned_op(self, op, qbit_list):
		"""
		qbit_reorder is 'visually correct'. So [a,b,c,d] implies bring to MSB 
		the bit in position 'a' in the original, brint to the next lower MSB 
		the bit in potion 'b' in the original, and so on ...
		"""
		qbit_reorder = self.__qbit_realign_list(qbit_list)
		(rmat,rrmat) = self.__rmat_rrmat(qbit_reorder)
		a_op = rrmat * op * rmat
		return a_op

	## __stretched_mat() and __aligned_op() use two concepts core to
	## the working of this simulator.

	def __stretched_mat(self,oper,qbit_list):
		orignm = oper[0]
		op = oper[1]
		opargs = str(qbit_list)
		if (op.shape)[1] != (op.shape)[0]:
			errmsg = f"Error. Operator is not a square matrix. {orignm}'s dimension = {op.shape}."
			raise QSimError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = f"User Error. Wrong number of qbit args for operator {orignm}. Provided arguments = {opargs}."
			raise QSimError(errmsg)
		c_op = np.kron(op,np.eye(2**(self.nqbits-len(qbit_list))))
		a_op = self.__aligned_op(c_op,qbit_list)
		return a_op

	def qstretch(self,oper,qbit_list):
		return ["{0:d}Q-{1:s}{2:s}".format(self.nqbits,oper[0],str(qbit_list)),self.__stretched_mat(oper,qbit_list)]

	def qinverse(self,op,name=None):
		if name is None:
			name = "INV-"+op[0]
		mat = deepcopy(op[1])
		invmat = np.conjugate(np.transpose(mat))
		return [name,invmat]

	def qisunitary(self,op):
		mat = op[1]
		(r,c) = mat.shape
		if r != c:
			return False
		invmat = np.conjugate(np.transpose(mat))
		pmat = np.asarray(mat * invmat)
		for i in range(r):
			for j in range(c):
				if i != j:
					if np.absolute(pmat[i][j]) > self.maxerr:
						return False
				else:
					if np.absolute(pmat[i][j]-1.0) > self.maxerr:
						return False
		return True


if __name__ == "__main__":
	pass