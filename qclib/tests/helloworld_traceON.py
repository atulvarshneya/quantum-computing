import qclib

print
print "Apply H on 0 then C on 0,3 then Measure 0"
qc = qclib.qcsim(8, qtrace=True)
qc.qgate(qc.H(),[0])
qc.qgate(qc.C(),[0,3])
qc.qmeasure([0])
