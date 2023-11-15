import qsim

q = qsim.QSimulator(4,qtrace=True,qzeros=True,visualize=True)

q.qgate(qsim.H(),[1])
q.qgate(qsim.C(),[1,0])
q.qreport(header="Probing states",probestates=[0,1,2,3])
q.qgate(qsim.H(),[2])
q.qgate(qsim.H(),[3])
