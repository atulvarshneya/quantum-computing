import qclib

q = qclib.qcsim(4)

q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),display=True)

q = qclib.qcsim(4)
q.qgate(q.H(),[0])
q.qgate(q.X(),[1])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),display=True)

q = qclib.qcsim(4)
q.qgate(q.X(),[0])
q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),display=True)
q = qclib.qcsim(4)
q.qgate(q.X(),[0])
q.qgate(q.H(),[0])
q.qgate(q.X(),[1])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),display=True)
