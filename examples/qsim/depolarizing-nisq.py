#!/usr/bin/env python

import qsim
import qsim.qnoisemodel
import numpy as np

print('Adding noise channel to all gates')
print()

# noise_model = {
# 	'noise_opseq_allgates': noise_opseq,       # e.g., [bit_flip(0.1), amplitude_damping(0.15), phase_damping(0.1)]
# 	'noise_opseq_init': noise_opseq,           # e.g., [bit_flip(0.1), phase_flip(0.1)]
# 	'noise_opseq_qubits': noise_opseq_applier  # e.g., [(depolarizing(0.1),[0,1]), ()]
# }

# with probabilty = 0.75, the bell-state gets completely depolarized (TODO source of this info?)
# i.e., becomes 1/4*I
noise_op = qsim.qnoisemodel.depolarizing(probability=0.75)
noise_model = {
    'noise_opseq_allgates': [noise_op]
}
q = qsim.NISQSimulator(2, noise_model=noise_model, qtrace=True, verbose=False)

q.qgate(qsim.H(),[0])
_,state,_ = q.qsnapshot()
print('Full state dump:')
print(state)
print(f'State trace {np.trace(state):.4f}')
print()

q.qgate(qsim.C(),[0,1])
_,state,_ = q.qsnapshot()
print('Full state dump:')
print(state)
print(f'State trace {np.trace(state):.4f}')
print()

I = ['Identity',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
q.qgate(I,[0])
_,state,_ = q.qsnapshot()
print('Full state dump:')
print(state)
print(f'State trace {np.trace(state):.4f}')
print()
