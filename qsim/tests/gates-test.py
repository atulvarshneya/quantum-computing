
import qsim

q = qsim.QSimulator(4,qtrace=True)

## X gate
q.qgate(q.X(),[0])
q.qgate(q.X(),[1])
q.qgate(q.X(),[2])
q.qgate(q.X(),[3])

# Y gate
q.qgate(q.Y(),[0])
q.qgate(q.Y(),[1])
invY = q.qinverse(q.Y())
q.qgate(invY,[1])
q.qgate(invY,[0])

# Z gate
q.qgate(q.Z(),[0])
q.qgate(q.Z(),[1])
q.qgate(q.Z(),[2])
q.qgate(q.Z(),[3])

# H gate
q.qreset()
q.qgate(q.H(),[2])
q.qgate(q.H(),[3])
q.qgate(q.C(),[2,0])
q.qgate(q.C(),[3,1])

# Rphi gate
q.qreset()
q.qgate(q.X(),[0])
q.qgate(q.X(),[1])
q.qgate(q.Rphi(q.pi/2),[0])
q.qgate(q.Rphi(q.pi/4),[1])

# SWAP
q.qreset()
q.qgate(q.X(),[0])
q.qgate(q.SWAP(),[0,1])
q.qgate(q.SWAP(),[3,1])

