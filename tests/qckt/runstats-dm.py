import numpy as np
import qckt
from qckt.backend import *

ck = qckt.QCkt(4)
ck.X(0)
ck.X(1)
ck.X(2)
ck.X(3)
ck.H(1)
ck.H(2)
ck.CX(1,2)
ck.draw()
job = qckt.Job(ck)
DMQdeb().runjob(job)

print('Total steps',job.runstats['QSteps'])
op_names = [k for k in job.runstats['OpCounts'].keys()]
op_names.sort() # so the print order is guaranteed to be the same each time
for k in op_names:
	print('op',k,'count',job.runstats['OpCounts'][k])

# Not using job.print_runstats(), as the actual execution time measurements will
# be slightly different for each run, so can lead to differnt output each time.
