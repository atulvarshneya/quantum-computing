#!/usr/bin/env python

import qckt
import qckt.backend as bknd

print("Services available")
svclist = bknd.Registry().listSvc()
for i in svclist: print(i[0],":", i[1])
print("-------------------------")
print()
usesvc = svclist[0][0]
print("Using service:",usesvc)
svc = bknd.Registry().getSvc('QSystems')
# print("Service object:", svc)
print("-------------------------")
print()
svcinsts = svc.listInstances()
print("Instances available:")
for i in svcinsts:
	print(i)
print("-------------------------")
print()
print('Using instance:','qsim-deb')
engine = svc.getInstance('qsim-deb')
print("-------------------------")
print()

ck = qckt.QCkt(4,4)
ck.H(0)
ck.CX(0,1)
ck.Border()
ck.X([2,3])
ck.Border()
ck.Probe("point 1")
ck.draw()

job = qckt.Job(ck,qtrace=False,shots=1)
engine.runjob(job)
print("-------------------------------")
print("printing results")
print(job.get_svec())
print(job.get_creg()[0])
