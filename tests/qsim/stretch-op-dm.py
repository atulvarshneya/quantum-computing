import qsim

qc = qsim.DMQSimulator(8,qtrace=True)
qc.qgate(qsim.H(),[3])
qc.qgate(qsim.C(),[3,0])

print()
print("------------------------------------------------------------")

qc = qsim.DMQSimulator(8,qtrace=True)
qc.qgate(qsim.H(),[3])
stC = qc.qstretch(qsim.C(),[3,0])
qc.qgate(stC,[7,6,5,4,3,2,1,0])
