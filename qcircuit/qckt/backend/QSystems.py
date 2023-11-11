#!/usr/bin/env python
import numpy as np
import qsim
from qckt.backend.BackendAPI import *
from qckt.qException import QCktException


class NISQeng:
	def __init__(self):
		pass

	def runjob(self, job):
		cregres_list = [None]*job.shots
		for shot_count in range(job.shots):
			qc = qsim.NISQSimulator(job.nqubits,job.nclbits,qtrace=False,verbose=job.verbose)
			if not job.noise_profile is None:
				kraus_spec = qc.qsim_noise_profile(**job.noise_profile)
				qc.qsim_noise_spec(kraus_spec)
			for op in job.assembledCkt:
				if op["op"] == "gate":
					if issubclass(type(op["qubits"][0]),list) and len(op["qubits"]) == 1:
						for q in op["qubits"][0]:
							qc.qgate([op["name"],op["opMatrix"]], [q], ifcbit=op["ifcbit"])
					else:
						qc.qgate([op["name"],op["opMatrix"]], op["qubits"], ifcbit=op["ifcbit"])
				elif op["op"] == "measure":
					qc.qmeasure(op["qubits"],cbit_list=op["clbits"])
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

class NISQdeb:
	def __init__(self):
		pass

	def runjob(self, job):
		cregres_list = [None]*job.shots
		if job.shots != 1:
			print("WARNING: debugger simulator, multi-shot not supported. Falling back to shots=1.")
		qc = qsim.NISQSimulator(job.nqubits,job.nclbits,qtrace=job.qtrace,verbose=job.verbose)
		if not job.noise_profile is None:
			kraus_spec = qc.qsim_noise_profile(**job.noise_profile)
			qc.qsim_noise_spec(kraus_spec)
		for op in job.assembledCkt:
			if op["op"] == "gate":
				if issubclass(type(op["qubits"][0]),list) and len(op["qubits"]) == 1:
					for q in op["qubits"][0]:
						qc.qgate([op["name"],op["opMatrix"]], [q], ifcbit=op["ifcbit"])
				else:
					qc.qgate([op["name"],op["opMatrix"]], op["qubits"], ifcbit=op["ifcbit"])
			elif op["op"] == "measure":
				qc.qmeasure(op["qubits"],cbit_list=op["clbits"])
			elif op["op"] == "probe":
				nqbits = job.nqubits
				ncbits = job.nclbits
				(creglist, sveclist, runstats) = qc.qsnapshot()
				print(op["header"])
				for i in range(len(sveclist)):
					if (op["probestates"] is None and abs(sveclist[i][i]) > 0.0) \
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
			elif op["op"] == "probe":
				nqbits = job.nqubits
				ncbits = job.nclbits
				(creglist, sveclist, runstats) = qc.qsnapshot()
				print(op["header"])
				for i in range(len(sveclist)):
					if (op["probestates"] is None and abs(sveclist[i]) > 0.0) \
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
	instances = {"qsim-eng":Qeng,"qsim-deb":Qdeb, 'nisqsim-eng':NISQeng, "nisqsim-deb":NISQdeb}

