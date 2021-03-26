import qsim

q = qsim.QSimulator(4)

q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),qtrace=True)

q = qsim.QSimulator(4)
q.qgate(q.H(),[0])
q.qgate(q.X(),[1])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),qtrace=True)

q = qsim.QSimulator(4)
q.qgate(q.X(),[0])
q.qgate(q.H(),[0])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),qtrace=True)
q = qsim.QSimulator(4)
q.qgate(q.X(),[0])
q.qgate(q.H(),[0])
q.qgate(q.X(),[1])
q.qgate(q.C(),[0,1])
q.qmeasure([0,1],basis=q.BELL_BASIS(),qtrace=True)
