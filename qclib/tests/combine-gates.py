#!/usr/bin/python

import qclib

print
print "Parallel HHHH and CCCC---------------------------------"
qc = qclib.qcsim(8)
H4 = qc.qcombine_par("H4",[qc.H(),qc.H(),qc.H(),qc.H()])
C4 = qc.qcombine_par("C4",[qc.C(),qc.C(),qc.C(),qc.C()])
qc.qgate(H4,[7,5,3,1], qtrace=True)
qc.qgate(C4,[7,6,5,4,3,2,1,0], qtrace=True)
qc.qgate(qc.C(),[7,6])
qc.qgate(qc.C(),[5,4])
qc.qgate(qc.C(),[3,2])
qc.qgate(qc.C(),[1,0])
qc.qreport("AFTER 4 individual C's")
qc.qgate(qc.H(),[7])
qc.qgate(qc.H(),[5])
qc.qgate(qc.H(),[3])
qc.qgate(qc.H(),[1])
qc.qreport("AFTER 4 individual H's")

print
print "Sequence HXYZ------------------------------------------"
qc = qclib.qcsim(8,qtrace=True)
HXYZ = qc.qcombine_seq("HXYZ",[qc.H(),qc.X(),qc.Y(),qc.Z()])
ZYXH = qc.qcombine_seq("ZYXH",[qc.Z(),qc.Y(),qc.X(),qc.H()])
qc.qgate(HXYZ,[0],qtrace=True)
qc.qgate(qc.Z(),[0],qtrace=True)
qc.qgate(qc.Y(),[0],qtrace=True)
qc.qgate(qc.X(),[0],qtrace=True)
qc.qgate(qc.H(),[0],qtrace=True)
