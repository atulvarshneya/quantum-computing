#!/usr/bin/python3

import numpy as np
import qckt
import GatesUtils as gutils
import Registers as regs

class QPE:
	def __init__(self, uop, uop_qubits, measurement_qubits):
		self.measurement_qubits = measurement_qubits
		self.uop_qubits = uop_qubits
		self.uop = uop
		self.nqubits = len(measurement_qubits) + len(uop_qubits)
		self.qpe_circuit = None

		qc = qckt.QCkt(self.nqubits)

		# Initialize the qubits, all counting qubits H
		qc.H(measurement_qubits)

		# Apply the controlled unitary operators in sequence
		cuop = gutils.CTL(self.uop)
		len_measq = len(measurement_qubits)
		repetitions = 1
		for ctrl_qubit in range(len_measq):
			for r in range(repetitions):
				qc.CUSTOM("UOP", cuop, ([self.measurement_qubits[len_measq-ctrl_qubit-1]] + self.uop_qubits))
			repetitions *= 2

		# Apply the inverse quantum Fourier transform
		qftckt_qubits = regs.QRegister(len(self.measurement_qubits))
		nq,_,_,_ = regs.placement(qftckt_qubits)
		QFTinvOp = gutils.opmat_dagger(qckt.QCkt(nq).QFT(qftckt_qubits).to_opMatrix())

		qc.CUSTOM("QFTinv", QFTinvOp, measurement_qubits)
		qc.M(measurement_qubits)
		self.qpe_circuit = qc


	def getckt(self):
		return self.qpe_circuit






if __name__ == "__main__":
	n_counting_qubits = 4

	measurement_qubits = regs.QRegister(n_counting_qubits)
	target_qubit = regs.QRegister(1)
	nqubits,_,qplaced,_ = regs.placement(target_qubit, measurement_qubits)

	theta = 6.0/8.0
	uop = qckt.QCkt(1).P(2*np.pi*theta,0).to_opMatrix()
	# mycircuit = qpe_program(n, theta)
	mycircuit = qckt.QCkt(nqubits)
	mycircuit.X(target_qubit)
	qpeckt = QPE(uop, target_qubit, measurement_qubits).getckt()
	mycircuit = mycircuit.append(qpeckt)
	mycircuit.draw()

	####
	## run multiple shots display the bargraph of results
	## pick the one with max freq as teh result
	####

	readouts = {}
	maxreads = 0
	resvalue = None
	for i in range(100):
		bk = qckt.Backend()
		bk.run(mycircuit)

		readval = bk.get_creg().intvalue
		if readval in readouts.keys():
			readouts[readval] += 1
		else:
			readouts[readval] = 1
		if readouts[readval] > maxreads:
			resvalue = readval
			maxreads = readouts[readval]

	minkey = min(readouts.keys())
	maxkey = max(readouts.keys())

	barsize = 100
	barscale = float(barsize)/maxreads

	for i in range(minkey,maxkey+1):
		print("{:6d}  ".format(i),end="")
		if i in readouts.keys():
			for j in range(int(readouts[i]*barscale)):
				print("#",end="")
		print()

	print("Max frequency = ",maxreads)
	print(str(resvalue)+"/2**"+str(n_counting_qubits)," = ",float(resvalue)/(2**n_counting_qubits))
