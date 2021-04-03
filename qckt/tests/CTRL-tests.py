import qckt
import numpy as np


# CX
print("CX ---------------------------------------")
ck = qckt.QCkt(8)
ck.CX(2,1,0)
ck.X([4,5,6])
ck.CX(6,5,4,3)
ck.list()
ck.draw()
bk = qckt.Backend()
bk.run(ck,qtrace=True)


# CP
print("CP ---------------------------------------")
ck = qckt.QCkt(8)
ck.CP(np.pi/4,2,1,0)
ck.X([4,5,6,3])
ck.CP(np.pi/4,6,5,4,3)
ck.list()
ck.draw()
bk = qckt.Backend()
bk.run(ck,qtrace=True)


# CROTx
print("CROTk ------------------------------------")
ck = qckt.QCkt(8)
ck.CROTk(3,2,1,0)
ck.X([4,5,6,3])
ck.CROTk(3,6,5,4,3)
ck.list()
ck.draw()
bk = qckt.Backend()
bk.run(ck,qtrace=True)
