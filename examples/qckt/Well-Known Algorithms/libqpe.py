#!/usr/bin/env python

import numpy as np
import qckt
import qckt.gatesutils as gutils

class QPE:
	def __init__(self, uop, uop_qubits, measurement_qubits):
		self.measurement_qubits = measurement_qubits
		self.uop_qubits = uop_qubits
		self.uop = uop
		self.nqubits = max(measurement_qubits + uop_qubits) + 1
		self.qpe_circuit = None

		compact_measqubits = qckt.QRegister(len(self.measurement_qubits))
		compact_uopqubits = qckt.QRegister(len(self.uop_qubits))
		compact_cregister = qckt.CRegister(len(compact_measqubits))
		compact_nqubits,compact_nclbits,_,_ = qckt.placement(compact_uopqubits,compact_measqubits, compact_cregister)

		qc = qckt.QCkt(compact_nqubits)

		# Initialize the qubits, all counting qubits H
		qc.H(compact_measqubits)

		# Apply the controlled unitary operators in sequence
		cuop = gutils.CTL(self.uop)
		len_measq = len(compact_measqubits)
		repetitions = 1
		qc.custom_gate("UOP", cuop)
		for ctrl_qubit in range(len_measq):
			for r in range(repetitions):
				qc.UOP(*([compact_measqubits[len_measq-ctrl_qubit-1]] + compact_uopqubits))
			repetitions *= 2

		# Apply the inverse quantum Fourier transform
		qftckt_qubits = qckt.QRegister(len(self.measurement_qubits))
		nq,_,_,_ = qckt.placement(qftckt_qubits)
		ckt = qckt.QCkt(nq)
		ckt.QFT(*qftckt_qubits)
		mat = ckt.to_opMatrix()
		QFTinvOp = gutils.opmat_dagger(mat)

		qc.custom_gate("QFTinv", QFTinvOp).QFTinv(*compact_measqubits)
		qc = qc.realign(self.nqubits, 0, self.uop_qubits+self.measurement_qubits)

		self.qpe_circuit = qc

	def getckt(self):
		return self.qpe_circuit

