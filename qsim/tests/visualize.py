import qsim

q = qsim.QSimulator(4,qtrace=True,qzeros=True,visualize=True)

q.qgate(q.H(),[1])
q.qgate(q.C(),[1,0])
q.qreport(header="Probing states",probestates=[0,1,2,3])
q.qgate(q.H(),[2])
q.qgate(q.H(),[3])
