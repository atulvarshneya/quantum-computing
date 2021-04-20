import qsim
import qgates
from qSimException import *

print()
print("Apply H on 0 then C on 0,3 then Measure 0")
qc = qsim.QSimulator(8, qtrace=True)
qc.qgate(qgates.H(),[0])
qc.qgate(qgates.C(),[0,3])
qc.qmeasure([0])
