import qsim

print()
print("Apply H on 0 then C on 0,3 then Measure 0")
qc = qsim.NISQSimulator(8)
qc.qreport(header="Initial State")
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qreport()
qc.qmeasure([0])
qc.qreport()
