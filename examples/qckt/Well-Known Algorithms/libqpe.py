#!/usr/bin/env python

import numpy as np
import qckt
import qckt.gatesutils as gutils

class QPE:
	def __init__(self, target_uop, uop_qubits, measurement_qubits):
		self.qpe_circuit = None

		# create a user defined gate for controlled-uop
		ctrl_func_op = gutils.CTL(target_uop)
		qckt.define_gate("CUOP", ctrl_func_op)

		# also create inverse quantum Fourier transform gate
		nqft = len(measurement_qubits)
		qftckt_qubits = [i for i in reversed(range(nqft))]
		ckt = qckt.QCkt(nqft)
		ckt.QFT(*(qftckt_qubits))
		mat = ckt.to_opMatrix()
		QFTinvOp = gutils.opmat_dagger(mat)
		qckt.define_gate("QFTinv", QFTinvOp)

		# start the QPE circuit
		nqubits = len(measurement_qubits + uop_qubits)
		qc = qckt.QCkt(nqubits)

		# put all measuremnt qubits in full superposition
		qc.H(measurement_qubits)

		# Apply the controlled unitary operators in sequence
		len_measq = len(measurement_qubits)
		uop_exponent = 1
		for ctrl_qubit in range(len_measq):
			for r in range(uop_exponent):
				qc.CUOP(*([measurement_qubits[len_measq-ctrl_qubit-1]] + uop_qubits))
			uop_exponent *= 2

		# complete the circuit with inverse-QFT on measurement_qubits
		qc.QFTinv(*measurement_qubits)

		self.qpe_circuit = qc

	def getckt(self):
		return self.qpe_circuit

