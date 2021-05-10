import qckt
from QSystems import *

ck1 = qckt.QCkt(4)
ck1.X([0,1])
ck1.H(0)
ck1.CX(0,1,2)
ck1.P(3.14/2,2)
ck1.CROTk(4,2,3)
ck1.CCX(1,2,3)
ck1.Probe("Expanded Circuit")
ck1.draw()
op = ck1.to_opMatrix()

bk = Backend()
bk.run(ck1)
svec1 = bk.get_svec()

print("====================================")

ck2 = qckt.QCkt(4)
ck2.CUSTOM("CKT",op,[3,2,1,0])
ck2.Probe("Circuit to_opMatrix()")
ck2.draw()

bk = Backend()
bk.run(ck2)
svec2 = bk.get_svec()


### compare the two svecs
res = True
if len(svec1.value) != len(svec2.value):
	print("ERROR - svecs are different - lengths unequal",len(svec1),len(svec2))
	res = False
else:
	for i in range(len(svec1.value)):
		if svec1.value[i] != svec2.value[i]:
			print("ERROR - svecs are different",i,": ",svec1.value[i], " != ",svec2.value[i])
			res = False
if res:
	print()
	print("===================")
	print("BOTH SVECS ARE SAME")
	print("===================")
