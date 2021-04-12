#!/usr/bin/python3

import qckt as q
from qException import QCktException

ck = q.QCkt(4)

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
	ck.CX(0,1)
	ck.CX(1)
except QCktException as e:
	print(e)

try:
	ck.QFT([0,1,2,3])
	ck.QFT([0,1],[2,3])
except QCktException as e:
	print(e)

try:
	ck.CX([0,1,2,3])
except QCktException as e:
	print(e)

