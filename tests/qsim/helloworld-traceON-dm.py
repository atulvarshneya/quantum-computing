import qsim

print()
print("Apply H on 0 then C on 0,3 then Measure 0")
qc = qsim.DMQSimulator(8, qtrace=True)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qmeasure([0])
