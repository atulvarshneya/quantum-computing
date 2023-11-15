
import qsim

q = qsim.NISQSimulator(4,qtrace=True)

# H gate
q.qgate(qsim.H(),[2])
q.qgate(qsim.H(),[3])
# C gate
q.qgate(qsim.C(),[2,0])
q.qgate(qsim.C(),[3,1])

## X gate
q.qgate(qsim.X(),[0])
q.qgate(qsim.X(),[1])
q.qgate(qsim.X(),[2])
q.qgate(qsim.X(),[3])

print('Total operation steps', q.qsteps)
op_names = [k for k in q.op_counts]
op_names.sort()
for k in op_names:
	print('    ',k, q.op_counts[k])
