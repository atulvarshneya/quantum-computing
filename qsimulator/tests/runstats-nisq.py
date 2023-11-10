
import NISQsim
import qgates
from qSimException import *

q = NISQsim.NISQSimulator(4,qtrace=True)

# H gate
q.qgate(qgates.H(),[2])
q.qgate(qgates.H(),[3])
# C gate
q.qgate(qgates.C(),[2,0])
q.qgate(qgates.C(),[3,1])

## X gate
q.qgate(qgates.X(),[0])
q.qgate(qgates.X(),[1])
q.qgate(qgates.X(),[2])
q.qgate(qgates.X(),[3])

print('Total operation steps', q.qsteps)
op_names = [k for k in q.op_counts]
op_names.sort()
for k in op_names:
	print('    ',k, q.op_counts[k])
