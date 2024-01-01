#!/usr/bin/env python3

import qckt.Canvas as cnv
import qckt.Gates as gts
import qckt.gatesutils as gutils
import qckt.noisemodel as ns
from qckt.qException import QCktException
# import qsim
# import numpy as np

class GateWrapper:
	def __init__(self, qckt, gateCls):
		self.qckt = qckt
		self.GateCls = gateCls
		# self.GateClsKraus = None
	def __call__(self, *args, **kwargs):
		gateObj = self.GateCls(*args, **kwargs)
		self.qckt.circuit.append(gateObj)
		if gateObj.check_qbit_args(self.qckt.nqubits) == False:
			raise QCktException(f"Error: qubit arguments incorrect. {gateObj.name}{str(gateObj.qbits)}")
		return gateObj
	def add_noise_to_all(self, kraus_ops):
		# don't need to check KrausOperator or KrausOperatorSequence, consolidate_gate_noise() checks that and converts
		self.GateCls.gatecls_kraus_ops = kraus_ops


class QCkt:

	def __init__(self, nqubits, nclbits=0, name=None, noise_model=None):
		self.nqubits = nqubits
		self.nclbits = nclbits
		self.circuit = []
		self.custom_gatescls_list = []
		self.name = name
		self.canvas = cnv.Canvas(self)
		self.add_noise_model(noise_model)

		for gclass in gts.GatesList:
			setattr(self, gclass.__name__, GateWrapper(self,gclass))
		## now create and register the classic CUSTOM gate. Need to deprecate that
		self.deprecated_custom_gate()

		self.idx = 0 # for iterations

	def __iter__(self):
		self.it = iter(self.circuit)
		return self
	def __next__(self):
		return next(self.it)

	def append(self, otherckt):
		# otherckt - the ckt to be appended
		nq = max(self.nqubits, otherckt.nqubits)
		nc = max(self.nclbits, otherckt.nclbits)
		newckt = QCkt(nq,nc,name=self.name)

		# copy over custom gate defs to new circuit
		newckt.__copyover_custom_gatedefs__(srcckt=self)
		newckt.__copyover_custom_gatedefs__(srcckt=otherckt)

		# copy circuits over to the new circuit
		for g in self.circuit:
			newckt.circuit.append(g)
		for g in otherckt.circuit:
			newckt.circuit.append(g)

		return newckt

	# change the qubits order to a different order
	def realign(self, newnq, newnc, inpqubits):
		# newq and newc are the new sizes of the qubits register and clbits register
		# inpqubits gives the new positions of the qubits
		# See README.md for details
		if self.nqubits != len(inpqubits):
			errmsg = "Error: error aligning qubits, number of qubits do not match"
			raise QCktException(errmsg)
		newckt = QCkt(newnq, newnc, name=self.name)
		newckt.__copyover_custom_gatedefs__(srcckt=self)
		for g in self.circuit:
			galigned = g.realign(inpqubits)
			newckt.circuit.append(galigned)
		return newckt

	def __copyover_custom_gatedefs__(self, srcckt):
		# copy over custom gate defs from source circuit
		for gcls in srcckt.custom_gatescls_list:
			self.custom_gatescls_list.append(gcls)
			setattr(self, gcls.__name__, GateWrapper(self,gcls))


	def assemble(self):
		assembled = []
		if self.noise_model is not None and self.noise_model.kraus_opseq_init is not None:
			noise_wrapper = self.NOISE
			noise_cls = noise_wrapper.GateCls
			noise_gate = noise_cls(self.noise_model.kraus_opseq_init, list(range(self.nqubits)))
			assembled.append(noise_gate.assemble(self.noise_model))
		for gt in self.circuit:
			assembled.append(gt.assemble(self.noise_model))
			if type(gt) is not gts.NOISE:
				pass # add NOISE gate if noise_model.kraus_opseq_allsteps is not None
		return assembled

	def to_opMatrix(self):
		oplist = []
		for q in self.circuit:
			op = q.to_fullmatrix(self.nqubits)
			if op is not None: ## Border, Probe gates return None
				oplist.append(op)
		opmat = gutils.combine_opmatrices_seq(oplist)
		return opmat

	def add_noise_model(self, noise_model=None):
		fixed_noise_model = noise_model
		if noise_model is not None:
			# validate the keys in the dict for noise_model argument
			if type(noise_model) is not ns.NoiseModel:
				raise QCktException(f'ERROR: noise_model expected to be NoiseMdel object or None')

			# validate the kraus_opseq_init field
			opseq_init = noise_model.kraus_opseq_init
			if opseq_init is not None:
				if type(opseq_init) is ns.KrausOperatorSequence:
					pass
				elif type(opseq_init) is ns.KrausOperator:
					opseq_init = ns.KrausOperatorSequence(opseq_init)
				else:
					raise QCktException('ERROR: noise_model.kraus_opseq_init must be KrausOperatorSequence or KrausOperator object.')
				# if kraus_opseq_init is specified, it must have only 1-qubit kraus operators
				for op in opseq_init:
					if op.nqubits != 1:
						raise QCktException(f'ERROR: noise_opseq_init must use 1-qubit kraus operators')

			# validate the kraus_opseq_allgates field
			opseq_allgates = noise_model.kraus_opseq_allgates
			if opseq_allgates is not None:
				if type(opseq_allgates) is ns.KrausOperatorSequence:
					pass
				elif type(opseq_allgates) is ns.KrausOperator:
					opseq_allgates = ns.KrausOperatorSequence(opseq_allgates)
				else:
					raise QCktException('ERROR: noise_model.kraus_opseq_allgates must be KrausOperatorSequence or KrausOperator object.')

			# validate the kraus_opseq_qubits field
			opseq_qubits = noise_model.kraus_opseq_qubits
			if opseq_qubits is not None:
				if type(opseq_qubits) is not ns.KrausOperatorApplierSequense:
					raise QCktException('ERROR: noise_model["kraus_opseq_qubits"] must be KrausOperatorApplierSequense object.')

			fixed_noise_model = ns.NoiseModel(kraus_opseq_init=opseq_init, kraus_opseq_allgates=opseq_allgates, kraus_opseq_qubits=opseq_qubits)
		# save the noise_model
		self.noise_model = fixed_noise_model

	def get_size(self):
		return self.nqubits, self.nclbits

	def draw(self,show_noise=True):
		self.canvas.draw(show_noise=show_noise)

	def list(self):
		if self.name is not None:
			print(self.name)
		for g in self.circuit:
			print(g)

	def custom_gate(self, cgate_name, opMatrix):
		if not gutils.isunitary(opMatrix):
			errmsg = "Custom gate, "+cgate_name+", operator matrix is not unitary."
			raise QCktException(errmsg)
		new_custom = gts.fetch_custom_gateclass(cgate_name=cgate_name, opMatrix=opMatrix)
		new_custom.__name__ = cgate_name
		self.custom_gatescls_list.append(new_custom)
		setattr(self, cgate_name, GateWrapper(self,new_custom))
		return self

	def deprecated_custom_gate(self):
		new_custom = gts.fetch_deprecated_custom_gateclass()
		depr_cust_gamtename = 'CUSTOM'
		new_custom.__name__ = depr_cust_gamtename
		setattr(self, depr_cust_gamtename, GateWrapper(self,new_custom))


if __name__ == "__main__":
	pass
