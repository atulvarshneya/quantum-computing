
import qsim

q = qsim.NISQSimulator(4,qtrace=True)

## X gate
q.qgate(qsim.X(),[0])
q.qgate(qsim.X(),[1])
q.qgate(qsim.X(),[2])
q.qgate(qsim.X(),[3])

# Y gate
q.qgate(qsim.Y(),[0])
q.qgate(qsim.Y(),[1])
invY = q.qinverse(qsim.Y())
q.qgate(invY,[1])
q.qgate(invY,[0])

# Z gate
q.qgate(qsim.Z(),[0])
q.qgate(qsim.Z(),[1])
q.qgate(qsim.Z(),[2])
q.qgate(qsim.Z(),[3])

# H gate
q = qsim.NISQSimulator(4,qtrace=True)
q.qgate(qsim.H(),[2])
q.qgate(qsim.H(),[3])
q.qgate(qsim.C(),[2,0])
q.qgate(qsim.C(),[3,1])

# Rphi gate
q = qsim.NISQSimulator(4,qtrace=True)
q.qgate(qsim.X(),[0])
q.qgate(qsim.X(),[1])
q.qgate(qsim.Rphi(q.pi/2),[0])
q.qgate(qsim.Rphi(q.pi/4),[1])

# SWAP
q = qsim.NISQSimulator(4,qtrace=True)
q.qgate(qsim.X(),[0])
q.qgate(qsim.SWAP(),[0,1])
q.qgate(qsim.SWAP(),[3,1])

