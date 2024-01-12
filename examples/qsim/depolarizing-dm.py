#!/usr/bin/env python

import qsim
import qsim.noisemodel as nmdl
import numpy as np

print('Adding noise channel to all gates')
print()

# with probabilty = 0.75, the bell-state gets completely depolarized (TODO source of this info?)
# i.e., becomes 1/4*I
noise_allgates = nmdl.qNoiseChannelSequence(
    nmdl.depolarizing(probability=0.75),
)
noise_model = {
    'noise_chan_allgates': noise_allgates,
}
q = qsim.DMQSimulator(2, noise_profile=noise_model, qtrace=True, verbose=False)

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
