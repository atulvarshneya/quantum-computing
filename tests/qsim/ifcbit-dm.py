#!/usr/bin/env python

import qsim

q = qsim.DMQSimulator(5,qtrace=True)

q.qgate(qsim.X(),[0])
q.qmeasure([0])
q.qgate(qsim.X(),[1], ifcbit=(0,1))
q.qmeasure([1])
q.qgate(qsim.X(),[2], ifcbit=(3,0))
q.qmeasure([2])
