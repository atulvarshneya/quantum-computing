import NISQsim
import qgates
from qSimException import *

qc = NISQsim.QSimulator(8,qtrace=True)
qc.qgate(qgates.H(),[3])
qc.qgate(qgates.C(),[3,0])

print()
print("------------------------------------------------------------")

qc = NISQsim.QSimulator(8,qtrace=True)
qc.qgate(qgates.H(),[3])
stC = qc.qstretch(qgates.C(),[3,0])
qc.qgate(stC,[7,6,5,4,3,2,1,0])
