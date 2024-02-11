import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns
import numpy as np

# test 01 - custom gate
print('test 01 - custom gate') 
# create user defined gates
qckt.define_gate('myX', np.matrix([[0.0,1.0],[1.0,0.0]],dtype=complex))
qckt.define_gate('myCX', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,0.0,1.0],[0.0,0.0,1.0,0.0]],dtype=complex))
ck = qckt.QCkt(3,3)
ck.H(0)
ck.myCX(0,2)
ck.myX(0)
ck.myX(1)
ck.myX(2)
ck.draw()
job = qckt.Job(ck,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test 02 - realign should preserve the custom gate definitions
print('test 02 - realign should preserve the custom gate definitions')
ck2 = ck.realign(newnq=3,newnc=3,inpqubits=[1,2,0])
ck2.myX(0)
ck2.draw()
job = qckt.Job(ck2,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)

# test 03 - append should preserve custom gate definitions
print('test 03 - append should preserve custom gate definitions')
qckt.define_gate('my2CX', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,0.0,1.0],[0.0,0.0,1.0,0.0]],dtype=complex))
qckt.define_gate('my2X', np.matrix([[0.0,1.0],[1.0,0.0]],dtype=complex))
ck3 = qckt.QCkt(3,3)
ck3.H(0)
ck3.my2CX(0,1)

ck4 = qckt.QCkt(3,3)
ck4.my2X(2)

ck5 = ck3.append(ck4)
ck5.my2CX(0,1)
ck5.draw()
job = qckt.Job(ck5,qtrace=True, verbose=True)
bk = bknd.DMQdeb()
bk.runjob(job)
