import numpy
import qsim
import qgates
from qSimException import *

qc = qsim.QSimulator(8,qtrace=True)

print()
print("------------------------------------------------")
print("Demonstrating User-defined CNOT gate ...")
def myCNOT():
	return ["MY-CNOT", numpy.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)]
qc.qgate(qgates.H(),[4])
qc.qgate(myCNOT(),[4,7])
qc.qgate(qgates.C(),[4,7])
qc.qgate(qgates.H(),[4])

print()
print("------------------------------------------------")
print("Demonstrating User-defined Phase Rotation gate ...")
def myR(theta):
	c = numpy.cos(theta)
	s = numpy.sin(theta)
	return ["MY-Rotation({:0.4f})".format(theta), numpy.matrix([[1,0],[0,complex(c,s)]],dtype=complex)]
qc.qgate(qgates.X(),[5])
qc.qgate(myR(numpy.pi/2),[5])
