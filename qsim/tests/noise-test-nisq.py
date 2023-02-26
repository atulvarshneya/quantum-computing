#!/usr/bin/env python

import NISQsim
import qgates as qgt
import numpy as np

noise_profiles_list = [
	'BitFlip',
	'PhaseFlip',
	'Depolarizing',
	'AmplitudeDamping',
	# 'GeneralizedAmplitudeDamping',
	'PhaseDamping',
	'PauliChannel'
	]

# print the list of canned kraus channels
q = NISQsim.QSimulator(1,qtrace=False, verbose=False)
kraus_spec = list(q.qsim_noise_profile('LIST'))
kraus_spec.sort()
print(kraus_spec)
print()

for prname in noise_profiles_list:
	print('==========================================================================')
	print('Kraus Channel: ',prname)
	print('--------------------------------------------------------------------------')

	q = NISQsim.QSimulator(3,qtrace=True, verbose=True)

	kraus_spec = q.qsim_noise_profile(prname, p1=0.05, p2=0.05, p3=0.05)
	q.qsim_noise_spec(kraus_spec)

	q.qgate(qgt.X(),[0])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	q.qgate(qgt.H(),[0])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	q.qgate(qgt.X(),[1])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	q.qgate(qgt.H(),[1])
	_,state,_ = q.qsnapshot()
	print(state)
	print(f'State trace {np.trace(state):.4f}')
	print()

	# I = ['Identity',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
	# q.qgate(I,[0])
	# q.qmeasure([0])