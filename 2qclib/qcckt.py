
import os
import numpy as np
import qcgates
import qcutilsckt as uckt
import qcutilsgts as ugts
from qcerror import *
# import qcsim as qs

class QCCkt:


	def debug_dump(self):
		def pretty_print_matrix(m):
			(r,c) = m.shape
			for i in range(r):
				for j in range(c):
					print("({0.real:0.2f},{0.imag:.2f}j)".format(m[i,j]), end=" ")
				print()
		print("====DEBUG DUMP==============================================")
		print("nqubits: {}".format(self.nqubits))
		c = ckt.getckt()
		for g in c:
			print(g[0], g[2])
			pretty_print_matrix(g[1])
		print("============================================================")

	def __init__(self, nq):
		self.nqubits = nq
		self.ckt = []
		self.gt = qcgates.QCGates()
		self.qcu = uckt.QCUtilsCkt(nq)
		self.cust_gate_dict = {}

	def add(self, gtname, qubits):
		if not self.qcu.valid_qbit_list(qubits):
			raise QCError("parameters not valid {} for gate: {}".format(qubits,gtname))
		if not self.gt.validate_gate(gtname):
			raise QCError('Unknown gate: '+gtname)
		if not self.gt.validate_gate_args(gtname,qubits):
			raise QCError('Incorrect number of qubits: {0}, for gate: {1}'.format(len(qubits),gtname))
		gateop = self.gt.get_op_matrix(gtname)
		self.ckt.append([gtname,gateop,qubits])

	def getckt(self):
		return self.ckt

	## create custom gates
	def define_gate(self, qname, qmatrix):
		self.gt.define_gate(qname, qmatrix)

	## get all gate names
	def list_all_ops(self):
		return self.gt.list_all_ops()

if __name__ == "__main__":

	def gen_Rphi(phi): # example of a custome gate being created
		"""
		Phase rotation gate. Takes the Phi as an argument.
		"""
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		gtname = "Rphi({:0.2f})".format(phi)
		gtmatrix = np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)
		return (gtname,gtmatrix)

	def gen_Rk(k): # example of a custome gate being created
		"""
		Controlled Phase rotation gate. Takes the k as an argument to divide 2*pi by 2**k.
		"""
		ck = np.cos(2*np.pi/(2**k))
		sk = np.sin(2*np.pi/(2**k))
		gtname = "Rk({:d})".format(k)
		gtmatrix = np.matrix([ [1,0], [0,complex(ck,sk)]],dtype=complex)
		return (gtname,gtmatrix)

	def gen_QFT(nqbits): # example of a custome gate being created
		N = 2**nqbits # number of rows and cols
		theta = 2.0 * np.pi / N
		opmat = [None]*N
		for i in range(N):
			# print "row",i,"--------------------"
			row = []
			for j in range(N):
				pow = i * j
				pow = pow % N
				# print "w^",pow
				row.append(np.e**(1.j*theta*pow))
			opmat[i] = row
		# print opmat
		gtname = "QFT({:d})".format(nqbits)
		gtmatrix = np.matrix(opmat,dtype=complex) / np.sqrt(N)
		return (gtname,gtmatrix)

	def gen_Hn(n): # example of a custome gate being created
		"""
		H^n gate - very commonly used
		"""
		op_list = []
		for i in range(n):
			op_list.append(H())
		gtname = "Hn({:d})".format(n)
		gtmatrix = ugts.qcombine_par(op_list)
		return (gtname,gtmatrix)

	##
	## Typical way to create a QC circuit
	##
	try:
		NQUBITS = 5
		ckt = QCCkt(NQUBITS)
		(rk4, gmat) = gen_Rk(4)
		ckt.define_gate(rk4, gmat)
		(rphi,gmat) = gen_Rphi(1.0)
		ckt.define_gate(rphi, gmat)

		ckt.add("H",[0])
		ckt.add("C", [1,0])
		ckt.add("T", [2,1,0])
		ckt.add("X",[1])
		ckt.add("Y",[2])
		ckt.add("Z",[3])
		ckt.add(rk4, [0])
		ckt.add(rphi, [0])
		ckt.add("M",[0,1])
	except QCError as err:
		print(err)
		quit()
	
	c = ckt.getckt()
	# and then create an instance of a QC machine and call run() on it with this circuit as input.
	# import qcsim
	# S = # initial state
	# exec = qcsim.QCExec(5,initstate=S)
	# meas_results = exec.run(ckt=c)

	ckt.debug_dump()
