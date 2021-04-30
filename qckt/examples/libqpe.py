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
		self.nqubits = max(measurement_qubits + uop_qubits) + 1
		self.qpe_circuit = None

		compact_measqubits = regs.QRegister(len(self.measurement_qubits))
		compact_uopqubits = regs.QRegister(len(self.uop_qubits))
		compact_cregister = regs.CRegister(len(compact_measqubits))
		compact_nqubits,compact_nclbits,_,_ = regs.placement(compact_uopqubits,compact_measqubits, compact_cregister)

		qc = qckt.QCkt(compact_nqubits)

		# Initialize the qubits, all counting qubits H
		qc.H(compact_measqubits)

		# Apply the controlled unitary operators in sequence
		cuop = gutils.CTL(self.uop)
		len_measq = len(compact_measqubits)
		repetitions = 1
		for ctrl_qubit in range(len_measq):
			for r in range(repetitions):
				qc.CUSTOM("UOP", cuop, ([compact_measqubits[len_measq-ctrl_qubit-1]] + compact_uopqubits))
			repetitions *= 2

		# Apply the inverse quantum Fourier transform
		qftckt_qubits = regs.QRegister(len(self.measurement_qubits))
		nq,_,_,_ = regs.placement(qftckt_qubits)
		QFTinvOp = gutils.opmat_dagger(qckt.QCkt(nq).QFT(qftckt_qubits).to_opMatrix())

		qc.CUSTOM("QFTinv", QFTinvOp, compact_measqubits)
		qc = qc.realign(self.nqubits, 0, self.uop_qubits+self.measurement_qubits)

		self.qpe_circuit = qc

	def getckt(self):
		return self.qpe_circuit

