import NISQsim
import qgates
from qSimException import *

print()
print("Apply H on 0 then C on 0,3 then Measure 0")
qc = NISQsim.NISQSimulator(8)
qc.qreport(header="Initial State")
qc.qgate(qgates.H(),[0])
qc.qgate(qgates.C(),[0,3])
qc.qreport()
qc.qmeasure([0])
qc.qreport()
