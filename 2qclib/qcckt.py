
import os
import numpy as np
import qcgates as qcg
import qcutilsckt as uckt
from qcerror import *
# import qcsim as qs

class qcckt:

	def debug_dump(self):
		print("====DEBUG DUMP=============")
		print("nqubits: {}".format(self.nqubits))
		for q in self.ckt:
			print(q)
		print("===========================")

	def __init__(self, nq):
		self.nqubits = nq
		self.ckt = []
		self.gt = qcg.qcgates()
		self.qcu = uckt.QCUtilsCkt(nq)
		self.cust_gate_dict = {}

	def add(self, gtname, qubits):
		if not self.qcu.valid_qbit_list(qubits):
			raise QCError("parameters not valid {} for gate: {}".format(qubits,gtname))
		if not self.gt.validate_gate(gtname):
			raise QCError('Unknown gate: '+gtname)
		if not self.gt.validate_gate_args(gtname,qubits):
			raise QCError('Incorrect number of qubits: {0}, for gate: {1}'.format(len(qubits),gtname))
		gateop = self.gt.getop(gtname)
		self.ckt.append([gtname,gateop,qubits])

	def getckt(self):
		return self.ckt

	def list_gates(self):
		return self.gt.listops()

	## create custom gates
	def custom_gate(self, qname, qmatrix):
		self.gt.mkgate(qname, qmatrix)

if __name__ == "__main__":

	def Rphi(phi): # example 1 of a custome gate being created
		"""
		Phase rotation gate. Takes the Phi as an argument.
		"""
		cphi = np.cos(phi)
		sphi = np.sin(phi)
		gtname = "ROTphi({:0.4f})".format(phi)
		gtmatrix = np.matrix([[1,0],[0,complex(cphi,sphi)]],dtype=complex)
		return (gtname,gtmatrix)

	def Rk(k):
		"""
		Controlled Phase rotation gate. Takes the k as an argument to divide 2*pi by 2**k.
		"""
		ck = np.cos(2*np.pi/(2**k))
		sk = np.sin(2*np.pi/(2**k))
		gtname = "ROTk({:d})".format(k)
		gtmatrix = np.matrix([ [1,0], [0,complex(ck,sk)]],dtype=complex)
		return (gtname,gtmatrix)

	try:
		ckt = qcckt(5)
		(rk4, gmat) = Rk(4)
		ckt.custom_gate(rk4, gmat)
		(rphi,gmat) = Rphi(1.0)
		ckt.custom_gate(rphi, gmat)

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
	for g in c:
		print(g[0], g[2])


	ckt.debug_dump()
