#!/usr/bin/env python

import NISQsim
import qgates as qgt
import qgatesUtils as qgu
from qSimException import *

print()
print("Parallel HX--------------------------------------------")
qc = NISQsim.NISQSimulator(8)
hx = qgu.qcombine_par('HX',[qgt.H(),qgt.X()])
qc.qgate(hx,[7,6], qtrace=True)

print()
print("Parallel HHHH and CCCC---------------------------------")
qc = NISQsim.NISQSimulator(8)
H4 = qgu.qcombine_par("H4",[qgt.H(),qgt.H(),qgt.H(),qgt.H()])
C4 = qgu.qcombine_par("C4",[qgt.C(),qgt.C(),qgt.C(),qgt.C()])
qc.qgate(H4,[7,5,3,1], qtrace=True)
qc.qgate(C4,[7,6,5,4,3,2,1,0], qtrace=True)
qc.qgate(qgt.C(),[7,6])
qc.qgate(qgt.C(),[5,4])
qc.qgate(qgt.C(),[3,2])
qc.qgate(qgt.C(),[1,0])
qc.qreport(header="AFTER 4 individual C's")
qc.qgate(qgt.H(),[7])
qc.qgate(qgt.H(),[5])
qc.qgate(qgt.H(),[3])
qc.qgate(qgt.H(),[1])
qc.qreport(header="AFTER 4 individual H's")

print()
print("Sequence HXYZ------------------------------------------")
qc = NISQsim.NISQSimulator(8,qtrace=True)
HXYZ = qgu.qcombine_seq("HXYZ",[qgt.H(),qgt.X(),qgt.Y(),qgt.Z()])
ZYXH = qgu.qcombine_seq("ZYXH",[qgt.Z(),qgt.Y(),qgt.X(),qgt.H()])
qc.qgate(HXYZ,[0],qtrace=True)
qc.qgate(qgt.Z(),[0],qtrace=True)
qc.qgate(qgt.Y(),[0],qtrace=True)
qc.qgate(qgt.X(),[0],qtrace=True)
qc.qgate(qgt.H(),[0],qtrace=True)
