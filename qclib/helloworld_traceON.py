import qclib
qc = qclib.qcsim(8, qtrace=True)
qc.qgate(qc.H(),[0])
qc.qgate(qc.C(),[0,3])
qc.qmeasure(0)
