import numpy
import qsim

qc = qsim.DMQSimulator(8,qtrace=True)

print()
print("------------------------------------------------")
print("Demonstrating User-defined CNOT gate ...")
def myCNOT():
	return ["MY-CNOT", numpy.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)]
qc.qgate(qsim.H(),[4])
qc.qgate(myCNOT(),[4,7])
qc.qgate(qsim.C(),[4,7])
qc.qgate(qsim.H(),[4])

print()
print("------------------------------------------------")
print("Demonstrating User-defined Phase Rotation gate ...")
def myR(theta):
	c = numpy.cos(theta)
	s = numpy.sin(theta)
	return ["MY-Rotation({:0.4f})".format(theta), numpy.matrix([[1,0],[0,complex(c,s)]],dtype=complex)]
qc.qgate(qsim.X(),[5])
qc.qgate(myR(numpy.pi/2),[5])
