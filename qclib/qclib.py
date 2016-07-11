#!/usr/bin/python

import numpy as np
import random as rnd

class qclib:

	def __init__(self, nq, qtrace=False, qzeros=False):
		"""
		First argument gives the number of qbits in the system. The initialization
		sets all qbits to |0>.
		qtrace=True causes each operation (gate, measurement) to emit resulting state.
		qzeros=True prints even those whose amplitude is 0
		"""
		# System Variables
		self.nqbits = nq

		# Runtime Options
		self.trace = qtrace
		self.disp_zeros = qzeros

		# Convinience constants
		self.pi = np.pi

		# Initial State
		qbit = [None]*self.nqbits
		for i in range(self.nqbits):
			qbit[i] = np.transpose(np.matrix([1,0],dtype=complex))
		self.sys_state = qbit[self.nqbits-1]
		l = range(self.nqbits-1)
		l.reverse()
		for i in l:
			self.sys_state = np.kron(self.sys_state,qbit[i])
		if self.trace:
			self.qreport(header="Initial State")

	def shuffled_count(self, bitorder):
		"""
		An internal function. Please ignore.
		"""
		sz = len(bitorder)
		shuffled = []
		for i in range(2**sz):
			shfval = 0
			for b in range(sz):
				dstbit = bitorder[sz-b-1]
				shfval += (((i >> b) & 0x1) << dstbit)
			shuffled.append(shfval)
		return shuffled

	def composite_op(self, op, opqbits):
		"""
		An internal function. Please ignore.
		"""
		comp_op = op
		for i in range(self.nqbits-opqbits):
			comp_op = np.kron(comp_op,np.eye(2))
		return comp_op

	def aligned_op(self, op, qbit_reorder):
		"""
		An internal function. Please ignore.

		qbit_reorder is 'visually correct'. So [a,b,c,d] implies MSB to be 
		replaced by the bit in position 'a' in the original, next lower MSB 
		to be replaced by bit in potion 'b' in the original, and so on ...
		"""
		if self.nqbits != len(qbit_reorder):
			errmsg = "Internal Error. " + str(self.nqbits) + " qbit system. Alignment vector has incorrect size " + str(len(qbit_reorder))
			raise QClibError(errmsg)
		# this is the counting with the given bit ordering
		rr = self.shuffled_count(qbit_reorder)
		## create the rmat and rrmat
		imat = np.matrix(np.eye(2**self.nqbits))
		rmat = np.matrix(np.eye(2**self.nqbits))
		rrmat = np.matrix(np.eye(2**self.nqbits))
		for i in range(2**self.nqbits):
			s = rr[i]
			rmat[i] = imat[s]
			rrmat[s] = imat[i]
		a_op = rrmat * op * rmat
		return a_op

	def qbit_reorder_list(self, qbit_list):
		"""
		An internal function. Please ignore.
		"""
		reord_list = qbit_list
		for i in range(self.nqbits):
			if i not in reord_list:
				reord_list.append(i)
		return reord_list

	def qgate(self, oper, qbit_list, display=False):
		"""
		qgate() is the function to perform any quantum gate operation on the qbits.
		Example:
			import qclib
			q = qclib.qclib(8,qtrace=True)
			q.qgate(q.H(),[1])
			q.qgate(q.C(),[1,0])
			q.qmeasure(0)
			q.qmeasure(1)

		The above code initializes an 8 qbit system (all qbits set to |0>). In the 
		qclib() call, qtrace=True causes every gate operation to emit the resulting 
		state. In the qgate() call, setting display=True also enables the print out
		for that operation. Following is the output generated from the code given
		above.
			Initial State
			00000000    1.00000000+0.00000000j

			HADAMARD Qbit[1]
			00000000    0.70710678+0.00000000j
			00000010    0.70710678+0.00000000j

			C-NOT Qbit[1, 0]
			00000000    0.70710678+0.00000000j
			00000011    0.70710678+0.00000000j

			MEASURED Qbit[0] = 1 with probality = 0.5
			00000011    1.00000000+0.00000000j

			MEASURED Qbit[1] = 1 with probality = 1.0
			00000011    1.00000000+0.00000000j

		Please note, only the non-zero amplitude values are printed. To print the complete state, use
		qclib(8,qtrace=True,qzeros=True)

		After the initialization, the code performs a Hadamard on qbit 1, followed by a 
		Controlled NOT on qbit 0, with qbit 1 being the control qbit. Basically, gets 
		qbits 1 and 0 in bell state and all other qbits stay in |0> (i.e., the resulting 
		state is (|00000000> + |00000011>)/sqrt(2)). Last two operations in the code are 
		measurement operations, on qbit 0 and 1 respectively. The measurement operation 
		measures the qbit as |0> or |1> per the appropriate probability (qclib uses random() 
		to decide what measurement to simulate). Please note that based on the measurement
		the appropriate new state is achived. Cleary, the computations can continue after 
		measurement operations.
		"""

		opname = oper[0]
		opargs = str(qbit_list)
		op = oper[1]
		if (op.shape)[1] != (op.shape)[0]:
			errmsg = "Error. Operator is not a sqare matrix. Dimension = (",(op.shape)[0],",",(op.shape)[1],")."
			raise QClibError(errmsg)
		if (2**len(qbit_list)) != (op.shape)[0]:
			errmsg = "User Error. Wrong number of qbit args for operator "+opname+". Provided arguments = "+opargs+"."
			raise QClibError(errmsg)
		c_op = self.composite_op(op,len(qbit_list))
		reord_list = self.qbit_reorder_list(qbit_list)
		a_op = self.aligned_op(c_op,reord_list)
		self.sys_state = a_op * self.sys_state
		if display or self.trace:
			hdr = opname + " Qbit" + opargs
			self.qreport(header=hdr)

	def qgate_batch(self, op_arg_list, display=False):
		"""
		Not sure if this batch operation is of any use, but threw it in anyways...
		"""
		for o in op_arg_list:
			self.qgate(o[0],o[1],display=display)

	def qmeasure(self, qbit, display=False):
		"""
		The measurement operation measures the specified qbit. The measured value is 
		simulated to be per the appropriate probability (qclib uses random() to decide 
		what measurement to simulate. Note that based on the measurement, the
		appropriate new state is achived. Cleary, the computations can continue after
		measurement operations.

		If display is True, or if qtrace is True, the result is printed out.
		"""

		bitmask = 0x1<<qbit
		amp_0 = 0
		amp_1 = 0
		meas_0_state = self.sys_state
		meas_1_state = self.sys_state
		for i in range(len(self.sys_state)):
			if (i & bitmask) == 0:
				amp_0 += np.absolute(self.sys_state[i].item(0))**2
			else:
				amp_1 += np.absolute(self.sys_state[i].item(0))**2
		toss = rnd.random()
		if toss <= amp_0:
			for i in range(len(self.sys_state)):
				if (i & bitmask) != 0:
					meas_0_state[i] = 0
			meas_0_state = meas_0_state / np.sqrt(amp_0)
			self.sys_state = meas_0_state
			qbit_val = 0
			prob = amp_0
		else:
			for i in range(len(self.sys_state)):
				if (i & bitmask) == 0:
					meas_1_state[i] = 0
			meas_1_state = meas_1_state / np.sqrt(amp_1)
			self.sys_state = meas_1_state
			qbit_val = 1
			prob = amp_1
		if display or self.trace:
			hdr = "MEASURED Qbit[" + str(qbit) + "] = " + str(qbit_val) + " with probality = " + str(prob) 
			self.qreport(header=hdr)

	def qreport(self, header="State", st=None):
		"""
		print out state information. if st=None, the system state is printed.
		Else the passed state is printed.
		header is some text printed above the state information.
		"""
		if st == None:
			st = self.sys_state
		print header
		for i in range(len(st)):
			if self.disp_zeros or np.absolute(st[i]) != 0:
				print format(i,'0'+str(self.nqbits)+'b')+"    "+"{:.8f}".format(np.around(st[i].item(0),8))
		print

	def qstate(self):
		"""
		Returns the stae of the qbits in a Python array.
		"""
		state_array = np.squeeze(np.asarray(self.sys_state))
		return state_array
	def qsize(self):
		"""
		Returns the the number of qbits in the system.
		"""
		return self.nqbits

	def qtraceON(self, val):
		"""
		Set the value of qtrace.
		"""
		self.trace = val

	def qzerosON(self, val):
		"""
		Set the value of qzeros.
		"""
		self.disp_zeros = val

	## QC Gates
	def X(self):
		"""
		Pauli_X gate.
		"""
		return ["PAULI_X", np.matrix([[0,1],[1,0]],dtype=complex)]
	def Y(self):
		"""
		Pauli_Y gate.
		"""
		return ["PAULI_Y", np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
	def Z(self):
		"""
		Pauli_Z gate.
		"""
		return ["PAULI_Z", np.matrix([[1,0],[0,-1]],dtype=complex)]
	def H(self):
		"""
		Hadamard gate.
		"""
		sqr2 = np.sqrt(2)
		return ["HADAMARD", np.matrix([[1/sqr2,1/sqr2],[1/sqr2,-1/sqr2]],dtype=complex)]
	def R(self,phi):
		"""
		Phase rotation gate. Takes the Phi as an argument.
		"""
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		return ["R-PHI", np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)]
	def SWAP(self):
		"""
		Swap gate.
		"""
		return ["SWAP", np.matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)]
	def C(self):
		"""
		Controlled NOT gate.
		"""
		return ["C-NOT", np.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)]


class QClibError:
	def __init__(self,arg):
		self.args = arg

if __name__ == "__main__":
	q = qclib(8,qtrace=True)
	q.qtraceON(True)

	try:
		q.qgate(q.H(),[2])
		q.qgate(q.H(),[4])
		q.qgate(q.C(),[2,1])
		q.qgate(q.C(),[4,3])
		q.qtraceON(True)
		q.qmeasure(2)
		q.qmeasure(1)
		q.qreport()
	except QClibError, m:
		print m.args

	st = q.qstate()
	for i in range(len(st)):
		print '{:08b}'.format(i), st[i]
