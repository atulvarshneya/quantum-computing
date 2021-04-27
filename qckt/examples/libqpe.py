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


