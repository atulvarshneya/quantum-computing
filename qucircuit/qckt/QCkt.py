#!/usr/bin/env python3

import qckt.Canvas as cnv
import qckt.Gates as gts
import qckt.gatesutils as gutils
import qckt.noisemodel as ns
from qckt.qException import QCktException


class GateWrapper:
	def __init__(self, qckt, gateCls):
		self.qckt = qckt
		self.GateCls = gateCls
	def __call__(self, *args, **kwargs):
		gateObj = self.GateCls(*args, **kwargs)
		self.qckt.circuit.append(gateObj)
		if gateObj.check_qbit_args(self.qckt.nqubits) == False:
			raise QCktException(f"Error: qubit arguments incorrect. {gateObj.name}{str(gateObj.qbits)}")
		return gateObj
	def set_noise_on_all(self, noise_chan):
		# don't need to check NoiseChannel or NoiseChannelSequence, consolidate_gate_noise() checks that and converts
		self.qckt.noise_profile_gates[self.GateCls] = noise_chan


class QCkt:

	def __init__(self, nqubits, nclbits=0, name=None, noise_profile=None):
		self.nqubits = nqubits
		self.nclbits = nclbits
		self.circuit = []
		self.custom_gatescls_list = []
		self.name = name
		self.canvas = cnv.Canvas(self)
		self.noise_profile_gates = {}  # this stores a map with gateCls as key, and noise spec as value
		self.noise_profile = None  # set_noise_profile() below updates it
		self.set_noise_profile(noise_profile)

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

	def get_gates_list(self):
		gates_list = []
		for gclass in gts.GatesList:
			gates_list.append(gclass.__name__)
		for cust_class in self.custom_gatescls_list:
			gates_list.append(cust_class.__name__)
		return gates_list

	def append(self, otherckt, name=None):
		# otherckt - the ckt to be appended
		nq = max(self.nqubits, otherckt.nqubits)
		nc = max(self.nclbits, otherckt.nclbits)
		if name is None:
			name = self.name
		newckt = QCkt(nq,nc,name=name)

		# copy over custom gate defs to new circuit
		newckt.__copyover_custom_gatedefs__(srcckt=self)
		newckt.__copyover_custom_gatedefs__(srcckt=otherckt)

		newckt.__copyover_noise_profile_gates__(srcckt=self)
		newckt.__copyover_noise_profile_gates__(srcckt=otherckt)

		# copy circuits over to the new circuit
		for g in self.circuit:
			newckt.circuit.append(g)
		for g in otherckt.circuit:
			newckt.circuit.append(g)

		return newckt

	# change the qubits order to a different order
	def realign(self, newnq, newnc, inpqubits, name=None):
		# newq and newc are the new sizes of the qubits register and clbits register
		# inpqubits gives the new positions of the qubits
		# See README.md for details
		if self.nqubits != len(inpqubits):
			errmsg = "Error: error aligning qubits, number of qubits do not match"
			raise QCktException(errmsg)
		if name is None:
			name = self.name
		newckt = QCkt(newnq, newnc, name=name)

		newckt.__copyover_custom_gatedefs__(srcckt=self)
		newckt.__copyover_noise_profile_gates__(srcckt=self)

		for g in self.circuit:
			galigned = g.realign(inpqubits)
			newckt.circuit.append(galigned)
		return newckt

	def __copyover_custom_gatedefs__(self, srcckt):
		# copy over custom gate defs from source circuit
		for gcls in srcckt.custom_gatescls_list:
			self.custom_gatescls_list.append(gcls)
			setattr(self, gcls.__name__, GateWrapper(self,gcls))

	def __copyover_noise_profile_gates__(self, srcckt):
		# copy over noise_profile_gates from source circuit
		for gcls in srcckt.noise_profile_gates:
			self.noise_profile_gates[gcls] = srcckt.noise_profile_gates[gcls]



	def assemble(self):
		assembled = []
		if self.noise_profile is not None and self.noise_profile.noise_chan_init is not None:
			noise_wrapper = self.NOISE
			noise_cls = noise_wrapper.GateCls
			noise_gate = noise_cls(self.noise_profile.noise_chan_init, list(range(self.nqubits)))
			assembled.append(noise_gate.assemble(self.noise_profile, self.noise_profile_gates))
		for gt in self.circuit:
			assembled.append(gt.assemble(self.noise_profile, self.noise_profile_gates))
			if type(gt) is not gts.NOISE:
				if self.noise_profile is not None and self.noise_profile.noise_chan_allsteps is not None and gt.is_noise_step():
					noise_wrapper = self.NOISE
					noise_cls = noise_wrapper.GateCls
					for kop,qbt in self.noise_profile.noise_chan_allsteps:
						noise_gate = noise_cls(kop, qbt)
						assembled.append(noise_gate.assemble(self.noise_profile, self.noise_profile_gates))
		return assembled

	def to_opMatrix(self):
		oplist = []
		for q in self.circuit:
			op = q.to_fullmatrix(self.nqubits)
			if op is not None: ## Border, Probe gates return None
				oplist.append(op)
		opmat = gutils.combine_opmatrices_seq(oplist)
		return opmat

	def set_noise_profile(self, noise_profile=None):
		fixed_noise_profile = noise_profile
		if noise_profile is not None:
			# validate the keys in the dict for noise_profile argument
			if type(noise_profile) is not ns.NoiseProfile:
				raise QCktException(f'ERROR: noise_profile expected to be NoiseProfile object or None')

			# validate the noise_chan_init field
			opseq_init = noise_profile.noise_chan_init
			if opseq_init is not None:
				if type(opseq_init) is ns.NoiseChannelSequence:
					pass
				elif type(opseq_init) is ns.NoiseChannel:
					opseq_init = ns.NoiseChannelSequence(opseq_init)
				else:
					raise QCktException('ERROR: noise_profile.noise_chan_init must be NoiseChannelSequence or NoiseChannel object.')
				# if noise_chan_init is specified, it must have only 1-qubit noise channel
				for op in opseq_init:
					if op.nqubits != 1:
						raise QCktException(f'ERROR: noise_opseq_init must use 1-qubit noise channel')

			# validate the noise_chan_allgates field
			opseq_allgates = noise_profile.noise_chan_allgates
			if opseq_allgates is not None:
				if type(opseq_allgates) is ns.NoiseChannelSequence:
					pass
				elif type(opseq_allgates) is ns.NoiseChannel:
					opseq_allgates = ns.NoiseChannelSequence(opseq_allgates)
				else:
					raise QCktException('ERROR: noise_profile.noise_chan_allgates must be NoiseChannel or NoiseChannel object.')

			# validate the noise_chan_qubits field
			opseq_qubits = noise_profile.noise_chan_qubits
			if opseq_qubits is not None:
				if type(opseq_qubits) is not ns.NoiseChannelApplierSequense:
					raise QCktException('ERROR: noise_profile.noise_chan_qubits must be NoiseChannelApplierSequense object.')

			# validate the noise_chan_allsteps field
			opseq_allsteps = noise_profile.noise_chan_allsteps
			if opseq_allsteps is not None:
				if type(opseq_allsteps) is not ns.NoiseChannelApplierSequense:
					raise QCktException('ERROR: noise_profile.noise_chan_allsteps must be NoiseChannelApplierSequense object.')

			fixed_noise_profile = ns.NoiseProfile(noise_chan_init=opseq_init, noise_chan_allgates=opseq_allgates, noise_chan_qubits=opseq_qubits, noise_chan_allsteps=opseq_allsteps)
		# save the noise_profile
		self.noise_profile = fixed_noise_profile

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
