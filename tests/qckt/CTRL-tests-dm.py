import qckt
from qckt.backend import *
import numpy as np


# CX
print("CX ---------------------------------------")
ck = qckt.QCkt(8)
ck.CX(2,1,0)
ck.X([4,5,6])
ck.CX(6,5,4,3)
ck.list()
ck.draw()
job = qckt.Job(ck, qtrace=True)
DMQdeb().runjob(job)

# CY
print("CY ---------------------------------------")
ck = qckt.QCkt(8)
ck.CY(2,1,0)
ck.X([4,5,6])
ck.CY(6,5,4,3)
ck.list()
ck.draw()
job = qckt.Job(ck, qtrace=True)
DMQdeb().runjob(job)

# CZ
print("CZ ---------------------------------------")
ck = qckt.QCkt(8)
ck.CZ(2,1,0)
ck.X([3,4,5,6])
ck.CZ(6,5,4,3)
ck.list()
ck.draw()
job = qckt.Job(ck, qtrace=True)
DMQdeb().runjob(job)

# CP
print("CP ---------------------------------------")
ck = qckt.QCkt(8)
ck.CP(np.pi/4,2,1,0)
ck.X([4,5,6,3])
ck.CP(np.pi/4,6,5,4,3)
ck.list()
ck.draw()
job = qckt.Job(ck, qtrace=True)
DMQdeb().runjob(job)


# CROTx
print("CROTk ------------------------------------")
ck = qckt.QCkt(8)
ck.CROTk(3,2,1,0)
ck.X([4,5,6,3])
ck.CROTk(3,6,5,4,3)
ck.list()
ck.draw()
job = qckt.Job(ck, qtrace=True)
DMQdeb().runjob(job)
