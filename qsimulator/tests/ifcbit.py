#!/usr/bin/env python

import qsim
import qgates as qgt
from qSimException import *

q = qsim.QSimulator(5,qtrace=True)

q.qgate(qgt.X(),[0])
q.qmeasure([0])
q.qgate(qgt.X(),[1], ifcbit=(0,1))
q.qmeasure([1])
q.qgate(qgt.X(),[2], ifcbit=(3,0))
q.qmeasure([2])
