import qclib

print()
print("Apply H on 0 then C on 0,3 then Measure 0")
qc = qclib.qcsim(8)
qc.qreport(header="Initial State")
qc.qgate(qc.H(),[0])
qc.qgate(qc.C(),[0,3])
qc.qreport()
qc.qmeasure([0])
qc.qreport()
