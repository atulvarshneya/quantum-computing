#!/usr/bin/env python
import sys
import qsim
import qsim.noisemodel as nmdl
import qckt.noisemodel as ns
from qckt.backend.BackendAPI import *
from qckt.qException import QCktException

def convert_to_qsim_noise_op_applier_seq(qckt_noise_chan_applier_seq):
	qsim_noise_applier_seq = None
	if qckt_noise_chan_applier_seq is not None:
		qsim_noise_applier_seq = nmdl.qNoiseChannelApplierSequense()
		for chan,qbits in qckt_noise_chan_applier_seq:
			opname = chan.name
			noise_chan = chan.noise_chan
			nqubits = chan.nqubits
			qsim_op = nmdl.qNoiseChannel(name=opname,operator_prob_set=noise_chan,nqubits=nqubits)
			qsim_noise_applier_seq.add(noise_chan=qsim_op,qubit_list=qbits)
	return qsim_noise_applier_seq

def convert_to_qsim_noise_op_sequence(qckt_noise_chan_sequence):
	qsim_noise_opseq = None
	if qckt_noise_chan_sequence is not None:
		qsim_noise_opseq = nmdl.qNoiseChannelSequence()
		for chan in qckt_noise_chan_sequence:
			opname = chan.name
			opprobset = chan.noise_chan
			nqubits = chan.nqubits
			qsim_op = nmdl.qNoiseChannel(name=opname,operator_prob_set=opprobset,nqubits=nqubits)
			qsim_noise_opseq.add_noise_channel(qsim_op)
	return qsim_noise_opseq


class DMQeng:
	def __init__(self):
		pass

	def runjob(self, job):
		cregres_list = [None]*job.shots
		for shot_count in range(job.shots):
			qc = qsim.DMQSimulator(job.nqubits,job.nclbits,noise_profile=None,qtrace=False,verbose=job.verbose)
			for op in job.assembledCkt:
				if op["op"] == "gate":
					qckt_noise_op = op['noiseChan']
					qsim_noise_opseq = convert_to_qsim_noise_op_applier_seq(qckt_noise_op)
					qc.qgate([op["name"],op["opMatrix"]], op["qubits"], ifcbit=op["ifcbit"],noise_chan=qsim_noise_opseq)
				elif op["op"] == "measure":
					qc.qmeasure(op["qubits"],cbit_list=op["clbits"])
				elif op["op"] == "noise":
					qckt_noise_op = op['noiseChan']
					qsim_noise_opseq = convert_to_qsim_noise_op_sequence(op["noiseChan"])
					qc.qnoise(qsim_noise_opseq, op['qubits'])
				elif op["op"] == "probe":
					pass
				elif op["op"] == "noop":
					pass
				else:
					raise QCktException("Encountered unknown instruction: "+str(op["op"]))
			cregvec,statevecarr,runstats = qc.qsnapshot()
			cregres = Cregister()
			cregres.setvalue_vec(cregvec)
			cregres_list[shot_count] = cregres
		# store the last statevec as well, helps with debugging
		statevec = StateVector()
		statevec.value = statevecarr
		job.result = Result(cregvals=cregres_list,svecvals=statevec)
		job.runstats = runstats
		return self

class DMQdeb:
	def __init__(self):
		self.maxerr = 10**(-6)
		pass

	def runjob(self, job):
		cregres_list = [None]*job.shots
		if job.shots != 1:
			print("WARNING: debugger simulator, multi-shot not supported. Falling back to shots=1.")
		qc = qsim.DMQSimulator(job.nqubits,job.nclbits,noise_profile=None,qtrace=job.qtrace,verbose=job.verbose)
		for op in job.assembledCkt:
			if op["op"] == "gate":
				qckt_noise_op = op['noiseChan']
				qsim_noise_opseq = convert_to_qsim_noise_op_applier_seq(qckt_noise_op)
				qc.qgate([op["name"],op["opMatrix"]], op["qubits"], ifcbit=op["ifcbit"],noise_chan=qsim_noise_opseq)
			elif op["op"] == "measure":
				qc.qmeasure(op["qubits"],cbit_list=op["clbits"])
			elif op["op"] == "noise":
				qckt_noise_op = op['noiseChan']
				qsim_noise_opseq = convert_to_qsim_noise_op_sequence(op["noiseChan"])
				qc.qnoise(qsim_noise_opseq, op['qubits'])
			elif op["op"] == "probe":
				nqbits = job.nqubits
				ncbits = job.nclbits
				(creglist, sveclist, runstats) = qc.qsnapshot()
				print('\n'+op["header"])
				for i in range(len(sveclist)):
					if (op["probestates"] is None and abs(sveclist[i][i]) > self.maxerr) \
							or (op["probestates"] is not None and i in op["probestates"]):
						print(("{0:0"+str(nqbits)+"b}    ... | {1:.8f}").format(i, sveclist[i][i]))
				cregsz = len(creglist)
				print("CREGISTER: ",end="")
				for i in range(cregsz):
					print("{:01b}".format(creglist[i]),end="")
				print()
			elif op["op"] == "noop":
				pass
			else:
				raise QCktException("Encountered unknown instruction: "+str(op["op"]))
		cregvec,statevecarr,runstats = qc.qsnapshot()
		cregres = Cregister()
		cregres.setvalue_vec(cregvec)
		cregres_list = [cregres]
		statevec = StateVector()
		statevec.value = statevecarr
		job.result = Result(cregvals=cregres_list,svecvals=statevec)
		job.runstats = runstats
		return self

class Qeng:
	def __init__(self):
		pass

	def runjob(self, job):
		cregres_list = [None]*job.shots
		for shot_count in range(job.shots):
			qc = qsim.QSimulator(job.nqubits,job.nclbits,qtrace=False,verbose=job.verbose)
			for op in job.assembledCkt:
				if op["op"] == "gate":
					if issubclass(type(op["qubits"][0]),list) and len(op["qubits"]) == 1:
						for q in op["qubits"][0]:
							qc.qgate([op["name"],op["opMatrix"]], [q], ifcbit=op["ifcbit"])
					else:
						qc.qgate([op["name"],op["opMatrix"]], op["qubits"], ifcbit=op["ifcbit"])
				elif op["op"] == "measure":
					qc.qmeasure(op["qubits"],cbit_list=op["clbits"])
				elif op["op"] == "noise":
					pass
				elif op["op"] == "probe":
					pass
				elif op["op"] == "noop":
					pass
				else:
					raise QCktException("Encountered unknown instruction: "+str(op["op"]))
			cregvec,statevec,runstats = qc.qsnapshot()
			cregres = Cregister()
			cregres.setvalue_vec(cregvec)
			cregres_list[shot_count] = cregres
		job.result = Result(cregvals=cregres_list)
		job.runstats = runstats
		return self

class Qdeb:
	def __init__(self):
		self.maxerr = 10**(-6)
		pass

	def runjob(self, job):
		cregres_list = [None]*job.shots
		if job.shots != 1:
			print("WARNING: debugger simulator, multi-shot not supported. Falling back to shots=1.")
		qc = qsim.QSimulator(job.nqubits,job.nclbits,qtrace=job.qtrace,verbose=job.verbose)
		for op in job.assembledCkt:
			if op["op"] == "gate":
				if issubclass(type(op["qubits"][0]),list) and len(op["qubits"]) == 1:
					for q in op["qubits"][0]:
						qc.qgate([op["name"],op["opMatrix"]], [q], ifcbit=op["ifcbit"])
				else:
					qc.qgate([op["name"],op["opMatrix"]], op["qubits"], ifcbit=op["ifcbit"])
			elif op["op"] == "measure":
				qc.qmeasure(op["qubits"],cbit_list=op["clbits"])
			elif op["op"] == "noise":
				pass
			elif op["op"] == "probe":
				nqbits = job.nqubits
				ncbits = job.nclbits
				(creglist, sveclist, runstats) = qc.qsnapshot()
				print('\n'+op["header"])
				for i in range(len(sveclist)):
					if (op["probestates"] is None and abs(sveclist[i]) > self.maxerr) \
							or (op["probestates"] is not None and i in op["probestates"]):
						print(("{0:0"+str(nqbits)+"b}    {1:.8f}").format(i, sveclist[i]))
				cregsz = len(creglist)
				print("CREGISTER: ",end="")
				for i in range(cregsz):
					print("{:01b}".format(creglist[i]),end="")
				print()
			elif op["op"] == "noop":
				pass
			else:
				raise QCktException("Encountered unknown instruction: "+str(op["op"]))
		cregvec,statevecarr,runstats = qc.qsnapshot()
		cregres = Cregister()
		cregres.setvalue_vec(cregvec)
		cregres_list = [cregres]
		statevec = StateVector()
		statevec.value = statevecarr
		job.result = Result(cregvals=cregres_list,svecvals=statevec)
		job.runstats = runstats
		return self


class qsimSvc(BackendSvc):
	def __init__(self,connectionToken=None):
		# Most other services will actually open a connection to the service provider, authenticate, store the seeion object, etc.
		pass
	def listInstances(self):
		# Most other services will implement the protocol to reach the service through the session object, and fetch the list of instances
		return list(qsimSvc.instances.keys())
	def getInstance(self, instkey):
		if instkey in qsimSvc.instances.keys():
			retinst = qsimSvc.instances[instkey]
			return retinst()
		else:
			raise QCktException("No such quantum computing instance "+str(instkey))
	# in our case since the list of instances is fixed we have simply statically initialized it
	instances = {"qsim-eng":Qeng,"qsim-deb":Qdeb, 'dmqsim-eng':DMQeng, "dmqsim-deb":DMQdeb}

