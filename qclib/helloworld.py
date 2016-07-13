import qclib
qc = qclib.qcsim(8)
qc.qgate(qc.H(),[0])
qc.qgate(qc.C(),[0,3])
qc.qreport()
qc.qmeasure(0)
qc.qreport()
