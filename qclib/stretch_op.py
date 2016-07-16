import qclib

qc = qclib.qcsim(8,qtrace=True)
qc.qgate(qc.H(),[3])
qc.qgate(qc.C(),[3,0])

print
print "------------------------------------------------------------"

qc = qclib.qcsim(8,qtrace=True)
qc.qgate(qc.H(),[3])
stC = qc.qstretch(qc.C(),[3,0])
qc.qgate(stC,[7,6,5,4,3,2,1,0])
