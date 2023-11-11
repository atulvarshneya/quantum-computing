
import qckt
from qckt import QCktException
import numpy as np

print('X')
ck = qckt.QCkt(5,5)
ck.X(1).ifcbit(2,1)
ck.X([2,3]).ifcbit(2,1)
ck.draw()

print('Y')
ck = qckt.QCkt(5,5)
ck.Y(1).ifcbit(2,1)
ck.Y([1,3]).ifcbit(2,1)
ck.draw()

print('Z')
ck = qckt.QCkt(5,5)
ck.Z(1).ifcbit(2,1)
ck.Z([1,3]).ifcbit(2,1)
ck.draw()

print('H')
ck = qckt.QCkt(5,5)
ck.H(0).ifcbit(2,1)
ck.H([1,3]).ifcbit(2,1)
ck.draw()

print('CX')
ck = qckt.QCkt(5,5)
ck.CX(1,3).ifcbit(2,1)
ck.draw()

print('CY')
ck = qckt.QCkt(5,5)
ck.CY(0,2).ifcbit(3,1)
ck.draw()

print('CZ')
ck = qckt.QCkt(5,5)
ck.CZ(0,2).ifcbit(3,1)
ck.draw()

print('CCX')
ck = qckt.QCkt(5,5)
ck.CCX(0,3,2).ifcbit(3,1)
ck.draw()

print('SWAP')
ck = qckt.QCkt(5,5)
ck.SWAP(1,3).ifcbit(3,1)
ck.draw()

print('M')
ck = qckt.QCkt(5,5)
try:
	ck.M([1,2]).ifcbit(3,1)
except QCktException as ex:
	print(ex)
ck.draw()

print('Border')
ck = qckt.QCkt(5,5)
try:
	ck.Border().ifcbit(2,1)
except QCktException as ex:
	print(ex)
ck.draw()

print('Probe')
ck = qckt.QCkt(5,5)
try:
	ck.Probe().ifcbit(2,1)
except QCktException as ex:
	print(ex)
ck.draw()

print('QFT')
ck = qckt.QCkt(5,5)
ck.QFT([1,3,2]).ifcbit(2,1)
ck.draw()

print('RND')
ck = qckt.QCkt(5,5)
ck.RND(2).ifcbit(3,1)
ck.draw()

print('P')
ck = qckt.QCkt(5,5)
ck.P(0.1, 2).ifcbit(3,0)
ck.draw()

print('CP')
ck = qckt.QCkt(5,5)
ck.CP(0.1,1,3).ifcbit(3,0)
ck.draw()

print('UROTk')
ck = qckt.QCkt(5,5)
ck.UROTk(3,2).ifcbit(3,1)
ck.draw()

print('CROTk')
ck = qckt.QCkt(5,5)
ck.CROTk(3,1,3).ifcbit(3,0)
ck.draw()

print('Rx')
ck = qckt.QCkt(5,5)
ck.Rx(0.1, 3).ifcbit(3,0)
ck.draw()

print('CRx')
ck = qckt.QCkt(5,5)
ck.CRx(0.1, 3,4).ifcbit(2,1)
ck.draw()

print('Ry')
ck = qckt.QCkt(5,5)
ck.Ry(0.1,0).ifcbit(2,1)
ck.draw()

print('CRy')
ck = qckt.QCkt(5,5)
ck.CRy(0.3, 3,2).ifcbit(4,0)
ck.draw()

print('Rz')
ck = qckt.QCkt(5,5)
ck.Rz(1.1, 2).ifcbit(3,0)
ck.draw()

print('CRz')
ck = qckt.QCkt(5,5)
ck.CRz(1.5, 2,3,4).ifcbit(2,0)
ck.draw()

print('CUSTOM')
ck = qckt.QCkt(5,5)
opmat = np.matrix([
	[1,0,0,0],
	[0,1,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
ck.CUSTOM("CUST",opmat,[0,2]).ifcbit(3,1)
ck.draw()
