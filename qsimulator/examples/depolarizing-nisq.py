import NISQsim
import qgates as qgt
import numpy as np

prname = 'Depolarizing'

q = NISQsim.NISQSimulator(2,qtrace=True, verbose=False)

q.qgate(qgt.H(),[0])
_,state,_ = q.qsnapshot()
print('Full state dump:')
print(state)
print(f'State trace {np.trace(state):.4f}')
print()

q.qgate(qgt.C(),[0,1])
_,state,_ = q.qsnapshot()
print('Full state dump:')
print(state)
print(f'State trace {np.trace(state):.4f}')
print()

# with s (i.e., p1) = 0.75, the bell-state gets completely depolarized
# i.e., becomes 1/4*I
noise_profile = {'profile_id':prname, 'p1':0.75, 'p2':0.75, 'p3':0.75}
kraus_spec = q.qsim_noise_profile(**noise_profile)
q.qsim_noise_spec(kraus_spec)
print('Added kraus channel to all qubits BUT must apply to 1 qubit ????!!!!????')
print()

I = ['Identity',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
q.qgate(I,[0])
_,state,_ = q.qsnapshot()
print('Full state dump:')
print(state)
print(f'State trace {np.trace(state):.4f}')
print()

