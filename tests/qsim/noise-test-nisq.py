#!/usr/bin/env python

import qsim
import qsim.kraus
import numpy as np

kraus_channels = [
	'BitFlip',
	'PhaseFlip',
	'Depolarizing',
	'AmplitudeDamping',
	# 'GeneralizedAmplitudeDamping',
	'PhaseDamping',
	'PauliChannel'
	]

# print the list of canned kraus channels
q = qsim.NISQSimulator(1,qtrace=False, verbose=False)
kraus_chans = list(qsim.kraus.kraus_channel_list())
kraus_chans.sort()
print(kraus_chans)
print()

for kchanname in kraus_channels:
	print('==========================================================================')
	print('Kraus Channel: ',kchanname)
	print('--------------------------------------------------------------------------')

	q = qsim.NISQSimulator(3,qtrace=True, verbose=True)

	kraus_spec = qsim.kraus.kraus_channel_spec(kchanname)
	q.kraus_global(kraus_spec())

	q.qgate(qsim.X(),[0])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	q.qgate(qsim.H(),[0])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	q.qgate(qsim.X(),[1])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	q.qgate(qsim.H(),[1])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	# I = ['Identity',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
	# q.qgate(I,[0])
	# q.qmeasure([0])
