#!/usr/bin/env python

import numpy as np

# ABSTRACT class for backend services
class BackendSvc:
	'the service implments the methods to connect with the quantum computing service, i.e., the required protocol, etc. - config registry will provide the specifics e.g., IP address'
	def __init__(self,connectionToken=None):
		'connectionToken contains the credentials required to access the service; the type of this object is specific to the service'
		self.connnectionToken = connectionToken
		pass
	def listInstances(self):
		'provides a list of tuples (name, description) of all instances (quamtum computer) available at this service'
		pass
	def getInstance(self, name):
		'returns an object representation of the named instance(quantum computer)'
		pass

class Cregister:

	def __init__(self):
		self.value = None
		self.intvalue = None

	def __str__(self):
		creg_str = ""
		for i in (range(len(self.value))): # creg[0] is MSB
			creg_str = creg_str + "{0:01b}".format(self.value[i])
		# creg_str = creg_str + "\n"
		return creg_str

	def setvalue_vec(self,cbitsvec):
		intval = 0
		for i in range(len(cbitsvec)):
			intval = 2 * intval
			intval += cbitsvec[i]
		self.intvalue = intval
		self.value = cbitsvec


class StateVector:

	def __init__(self):
		self.value = None
		self.verbosity = False

	def __str__(self):
		svec_str = ""
		dispvalue = self.value
		if len(dispvalue.shape) > 1:
			svec_str = "Density matrix DIAGONAL\n"
			dispvalue = np.diagonal(self.value)

		### wonky way to find number of qubits
		nq = 0
		n = len(dispvalue) - 1
		while n > 0:
			nq = nq + 1
			n = n >> 1

		statefmt = "{0:"+"0{0:d}b".format(nq)+"}"
		s = 0
		for i in dispvalue:
			if self.verbosity or np.absolute(i) > 10**(-6):
				svec_str = svec_str + statefmt.format(s) + "  " + "{:.8f}".format(i) + "\n"
			s += 1
		return svec_str

	def verbose(self,v):
		if v is True:
			self.verbosity = True
		else:
			self.verbosity = False
		return self

class Result:
	def __init__(self,cregvals,svecvals=None):
		self.cregister = cregvals
		self.state_vector = svecvals

