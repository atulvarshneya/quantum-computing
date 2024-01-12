#!/usr/bin/python3

# This file is part of the QSIM project covered under GPL v3 license.
# See the full license in the file LICENSE
# Author: Atul Varshneya

from qsim.qSimException import QSimError
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

class QSimulator:

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
		if noise_profile is not None:
			print('WARNING: Ignoring unsupported argument noise_profile in QSimulator(). For noise simulation, use DM simulators.')

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
		print(f'WARNING: qreset() is deprecated. Reinstantiate the Qsimulator object instead.')
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
		else:
			# initialize the qbits to |0>
			qbit = [None]*self.nqbits
			for i in range(self.nqbits):
				qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
			# Now create the state as a tensor product of the qbits (MSB to the left)
			self.sys_state = qbit[self.nqbits-1]
			for i in reversed(range(self.nqbits-1)):
				self.sys_state = np.kron(qbit[i],self.sys_state)
		if self.trace:
			self.qreport(header="Initial State")


	def qnoise(self, noise_chan, qbit_list, qtrace=False):
		print('WARNING: Ignoring unsupported function qnoise(). For noise simulation, use DM simulators.')

	def qgate(self, oper, qbit_list, ifcbit=None, noise_chan=None, qtrace=False):  # ifcbit is encoded as tuple (cbit, ifvalue)
		if noise_chan is not None:
			print('WARNING: Ignoring unsupported argument noise_chan in qgate(). For noise simulation, use DM simulators.')

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
			self.sys_state = a_op * self.sys_state

		if qtrace or self.trace:
			opname = oper[0]
			opargs = str(qbit_list)
			cond_cbit_arg = '' if ifcbit is None else ' if Cbit'+str(ifcbit[0])+'='+str(ifcbit[1])
			hdr = opname + " Qubit" + opargs + cond_cbit_arg
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
		self.sys_state = rmat * self.sys_state

		list_len = len(qbit_list)
		qbitmask = 0
		for b in range(list_len):
			qbitmask |= 0x1 << (self.nqbits-b-1)
		shift_bits = self.nqbits - list_len

		# add up the probability of the various combinations of the qbits to measure
		prob = [0]*(2**list_len)
		for i in range(len(self.sys_state)):
			prob_idx = (i & qbitmask) >> shift_bits # Hmmm, could have kept the opposite bit order; too late now!!
			prob[prob_idx] += np.absolute(self.sys_state[i].item(0))**2
		# ... and verify the total probability adds up to 1.0, within the acceptable margin
		totprob = 0
		for p in prob:
			totprob += p
		if np.absolute(totprob - 1.0) > self.maxproberr:
			errmsg = "Internal error, total probability != 1  (total prob = {:f}".format(totprob)
			raise QSimError(errmsg)

		# OK, now see which one should be selected
		toss = rnd.random()
		sel = len(prob) - 1 # to default if all the probs add up just short of 1, and toss == 1
		prob_val = prob[sel]
		cumprob = 0
		for i in range(len(prob)):
			if toss > cumprob and toss <= (cumprob + prob[i]):
				sel = i
			cumprob += prob[i]
		prob_val = prob[sel]
		meas_val = []
		for i in reversed(range(list_len)):
			if (sel & (0x1<<i)) == 0:
				meas_val.append(0)
			else:
				meas_val.append(1)

		# now, collapse to the selected state (all other amplitudes = 0), and normlize the amplitudes
		to_match = sel << shift_bits
		for i in range(len(self.sys_state)):
			if (i & qbitmask) == to_match:
				self.sys_state[i] = self.sys_state[i] / np.sqrt(prob_val)
			else:
				self.sys_state[i] = 0

		# align the qbits back to original
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
		if probestates is not None:
			header = header + " - Probestates: "+str(probestates)
		print()
		print(header)
		for i in range(len(state)):
			if self.disp_zeros or np.absolute(state[i]) > self.maxerr:
				barlen = 20
				barstr = ""
				if self.visualize or visualize:
					barstr = "	x"
					amp = np.absolute(state[i].item(0))*barlen
					intamp = int(amp)
					if amp > self.maxerr:
						barstr = "	|"
						for b in range(barlen):
							if b <= intamp:
								barstr = barstr+"*"
							else:
								barstr = barstr + "."
				ststr = ("{:0"+str(self.nqbits)+"b}    ").format(i)
				ampstr = "{:.8f}".format(np.around(state[i].item(0),8))
				if probestates is None or i in probestates:
					print(ststr + ampstr + barstr)
		print("CREGISTER: ", end="")
		for i in range(self.ncbits): # cregister[0] is MSB
			print("{0:01b}".format(self.cregister[i]),end="")
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
			errmsg = "Error. Operator is not a square matrix. "+orignm+"'s dimension = ("+str((op.shape)[0])+","+str((op.shape)[1])+")."
			raise QSimError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = "User Error. Wrong number of qbit args for operator "+orignm+". Provided arguments = "+opargs+"."
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
