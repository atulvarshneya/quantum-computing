#!/usr/bin/env python

import qckt as q
from qckt import QCktException
import numpy as np

ck = q.QCkt(4,4)

try:
	ck.X(8)
except QCktException as e:
	print(e.msg)
try:
	ck.X(0)
	ck.X([0,1,2,6])
except QCktException as e:
	print(e)

try:
	ck.Y(8)
except QCktException as e:
	print(e.msg)
try:
	ck.Y(0)
	ck.Y([0,1,2,6])
except QCktException as e:
	print(e)

try:
	ck.Z(8)
except QCktException as e:
	print(e.msg)
try:
	ck.Z(0)
	ck.Z([0,1,2,6])
except QCktException as e:
	print(e)

try:
	ck.H(8)
except QCktException as e:
	print(e.msg)
try:
	ck.H(0)
	ck.H([0,1,6])
except QCktException as e:
	print(e)

try:
	ck.RND(8)
except QCktException as e:
	print(e.msg)
try:
	ck.RND(0)
	ck.RND([0,1,6])
except QCktException as e:
	print(e)

try:
	ck.P(3.14/2,8)
except QCktException as e:
	print(e.msg)
try:
	ck.P(3.14/2,0)
	ck.P(3.14/2,[0,1,6])
except QCktException as e:
	print(e)

try:
	ck.UROTk(12,8)
except QCktException as e:
	print(e.msg)
try:
	ck.UROTk(10,0)
	ck.UROTk(8,[0,1,6])
except QCktException as e:
	print(e)

try:
	ck.CX(0,1)
	ck.CX(1)
except QCktException as e:
	print(e)
try:
	ck.CX([0,1,2,3])
except QCktException as e:
	print(e)

try:
	ck.CY(0,1)
	ck.CY(1)
except QCktException as e:
	print(e)
try:
	ck.CY([0,1,2,3])
except QCktException as e:
	print(e)

try:
	ck.CZ(0,1)
	ck.CZ(1)
except QCktException as e:
	print(e)
try:
	ck.CZ([0,1,2,3])
except QCktException as e:
	print(e)

try:
	ck.CCX(0,1,2)
	ck.CCX(1,1,3)
except QCktException as e:
	print(e)
try:
	ck.CCX(1,2,8)
except QCktException as e:
	print(e)
try:
	ck.CCX([0,1],2,3)
except QCktException as e:
	print(e)

try:
	ck.CP(3.14/2,0,1)
	ck.CP(3.14/2, 0,1,2,3)
	ck.CP(3.14/2,1)
except QCktException as e:
	print(e)
try:
	ck.CP(3.14/2, 0,1,2,3)
	ck.CP(3.14/2, [0,1,2,3])
except QCktException as e:
	print(e)

try:
	ck.CROTk(2, 0,1)
	ck.CROTk(2, 0,1,2,3)
	ck.CROTk(2, 1)
except QCktException as e:
	print(e)
try:
	ck.CROTk(2, 0,1,2,3)
	ck.CROTk(2, 0,1,2,8)
except QCktException as e:
	print(e)

try:
	ck.QFT([0,1,2,3])
	ck.QFT([0,1],[2,3])
except QCktException as e:
	print(e)

try:
	ck.SWAP(0,1)
	ck.SWAP(0,8)
except QCktException as e:
	print(e)
try:
	ck.SWAP([0,1],[2,3])
except QCktException as e:
	print(e)

try:
	ck.M([0,1])
	ck.M([0,8])
except QCktException as e:
	print(e)
try:
	ck.M([0,1],[2,5])
except QCktException as e:
	print(e)
try:
	ck.M([0,2],[2,1,2])
except QCktException as e:
	print(e)

opmat = np.matrix([
	[1,0,0,0],
	[0,1,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
try:
	ck.CUSTOM("CNOT",opmat,[0,1])
	ck.CUSTOM("CNOT",opmat,[0,1,2])
except QCktException as e:
	print(e)

opmat = np.matrix([
	[1,0,0,0],
	[0,0,0,1],
	[0,0,1,0]],dtype=complex)
try:
	ck.CUSTOM("CTRLX",opmat,[0,1])
except QCktException as e:
	print(e)
