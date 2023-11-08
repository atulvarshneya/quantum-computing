
import NISQsim
import qgates
from qSimException import *

q = NISQsim.NISQSimulator(4,qtrace=True)

## X gate
q.qgate(qgates.X(),[0])
q.qgate(qgates.X(),[1])
q.qgate(qgates.X(),[2])
q.qgate(qgates.X(),[3])

# Y gate
q.qgate(qgates.Y(),[0])
q.qgate(qgates.Y(),[1])
invY = q.qinverse(qgates.Y())
q.qgate(invY,[1])
q.qgate(invY,[0])

# Z gate
q.qgate(qgates.Z(),[0])
q.qgate(qgates.Z(),[1])
q.qgate(qgates.Z(),[2])
q.qgate(qgates.Z(),[3])

# H gate
q.qreset()
q.qgate(qgates.H(),[2])
q.qgate(qgates.H(),[3])
q.qgate(qgates.C(),[2,0])
q.qgate(qgates.C(),[3,1])

# Rphi gate
q.qreset()
q.qgate(qgates.X(),[0])
q.qgate(qgates.X(),[1])
q.qgate(qgates.Rphi(q.pi/2),[0])
q.qgate(qgates.Rphi(q.pi/4),[1])

# SWAP
q.qreset()
q.qgate(qgates.X(),[0])
q.qgate(qgates.SWAP(),[0,1])
q.qgate(qgates.SWAP(),[3,1])

