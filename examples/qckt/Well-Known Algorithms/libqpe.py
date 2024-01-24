#!/usr/bin/env python

import numpy as np
import qckt
import qckt.gatesutils as gutils

class QPE:
	def __init__(self, target_uop, uop_qubits, measurement_qubits):
		self.qpe_circuit = None

		# start the QPE circuit
		nqubits = len(measurement_qubits + uop_qubits)
		qc = qckt.QCkt(nqubits)

		# put all measuremnt qubits in full superposition
		qc.H(measurement_qubits)

		# create a custom gate for controlled-uop
		ctrl_func_op = gutils.CTL(target_uop)
		qc.custom_gate("CUOP", ctrl_func_op)

		# Apply the controlled unitary operators in sequence
		len_measq = len(measurement_qubits)
		uop_exponent = 1
		for ctrl_qubit in range(len_measq):
			for r in range(uop_exponent):
				qc.CUOP(*([measurement_qubits[len_measq-ctrl_qubit-1]] + uop_qubits))
			uop_exponent *= 2

		# to apply the inverse quantum Fourier transform, first build the inverse-QFT gate
		nqft = len(measurement_qubits)
		qftckt_qubits = [i for i in reversed(range(nqft))]
		ckt = qckt.QCkt(nqft)
		ckt.QFT(*(qftckt_qubits))
		mat = ckt.to_opMatrix()
		QFTinvOp = gutils.opmat_dagger(mat)
		qc.custom_gate("QFTinv", QFTinvOp)

		# complete the circuit with inverse-QFT on measurement_qubits
		qc.QFTinv(*measurement_qubits)

		self.qpe_circuit = qc

	def getckt(self):
		return self.qpe_circuit

