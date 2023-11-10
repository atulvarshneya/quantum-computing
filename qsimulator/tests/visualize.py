import qsim
import qgates
from qSimException import *

q = qsim.QSimulator(4,qtrace=True,qzeros=True,visualize=True)

q.qgate(qgates.H(),[1])
q.qgate(qgates.C(),[1,0])
q.qreport(header="Probing states",probestates=[0,1,2,3])
q.qgate(qgates.H(),[2])
q.qgate(qgates.H(),[3])
