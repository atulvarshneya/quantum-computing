#!/usr/bin/env python

import qsim

q = qsim.DMQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.H(),[2])
q.qgate(qsim.C(),[2,1])
q.qreport('Entangled state')
q.qzerosON(True)
q.qmeasure([2,1])
q.qreport('Final state', probestates=[0,7])

