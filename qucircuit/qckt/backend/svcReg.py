#!/usr/bin/python3

import qckt.backend.QSystems as qsys
from qckt.qException import QCktException


class Registry:
	'this is an API for accessing the registry of Quantum Computing Services (e.g., IBM quantum computing, Ionq quantum computing, local qsim simulator, local debugging simulator)'
	services = {"QSystems": (qsys.qsimSvc, "qsim simulator from Quantum Systems")}

	def __init__(self):
		pass
	def listSvc(self):
		'returns a list of tuples (name, description) of all services available (i.e. registered in the configuration)'
		return [(k,Registry.services[k][1]) for k in Registry.services.keys()]
	def getSvc(self, svcName):
		if svcName in Registry.services.keys():
			return Registry.services[svcName][0]()
		else:
			raise QCktException("No such registered service: "+str(svcName))

