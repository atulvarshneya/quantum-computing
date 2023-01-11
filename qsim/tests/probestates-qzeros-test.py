#!/usr/bin/env python

import qsim
import qgates as qgt

q = qsim.QSimulator(3,qtrace=True, verbose=True)
q.qgate(qgt.H(),[2])
q.qgate(qgt.C(),[2,1])
q.qreport('Entangled state')
q.qzerosON(True)
q.qmeasure([2,1])
q.qreport('Final state', probestates=[0,7])

