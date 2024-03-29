#!/usr/bin/env python

import qsim
import qsim.noisemodel as nmdl


# print the list of canned kraus channels
noise_channels = list(nmdl.noise_channel_list().keys())
noise_channels.sort()
print(noise_channels)
print()

# test 01 - without any noise model
print('test 01 - without any noise model')
q = qsim.DMQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2])
q.qgate(qsim.H(),[2])

# test 02 - direct call to qnoise
print('test 02 - direct call to qnoise')
q = qsim.DMQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_chan=nmdl.qNoiseChannelSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2])
q.qgate(qsim.H(),[2])

# test 03 - adding noise applied to a gate invokation
print('test 03 - adding noise applied to a gate invokation')
q = qsim.DMQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_chan=nmdl.qNoiseChannelSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_chan=nmdl.qNoiseChannelSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])

# test 04 - adding noise applied to all gates
print('test 04 - adding noise at init, applied to specifc qubits, all gates')
noise_model = {
	'noise_chan_init': nmdl.qNoiseChannelSequence(nmdl.phase_flip(probability=0.2)),
	'noise_chan_allgates': nmdl.qNoiseChannelSequence(nmdl.depolarizing(probability=0.1)),
	'noise_chan_qubits': nmdl.qNoiseChannelApplierSequense(nmdl.qNoiseChannelSequence(nmdl.bit_flip(probability=0.3)),[1]),
}
q = qsim.DMQSimulator(3, noise_profile=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_chan=nmdl.qNoiseChannelSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_chan=nmdl.qNoiseChannelSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])

# test 05 - a blanket test for all noise operators applied to all gates, using their default arguments
for nchanid in noise_channels:
	if nmdl.noise_channel_lookup(nchanid)().nqubits != 1:
		# print(f'skipped {nchanid}')
		continue
	print(f'test 05 - Blanket test - {nchanid}')
	krfn = nmdl.noise_channel_lookup(nchanid)
	noise_model = {
		'noise_chan_allgates': nmdl.qNoiseChannelSequence(krfn()),
		'noise_chan_init': None
	}
	q = qsim.DMQSimulator(3, noise_profile=noise_model, qtrace=True, verbose=True)
	q.qgate(qsim.X(),[0])
	q.qnoise(noise_chan=nmdl.qNoiseChannelSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
	q.qgate(qsim.C(),[0,1])
	q.qgate(qsim.X(),[2], noise_chan=nmdl.qNoiseChannelSequence(nmdl.phase_flip(probability=0.1)))
	q.qgate(qsim.H(),[2])

# test 06 - 2-qubit noise op - two_qubit_dephasing
print('test 06 - adding noise at init, applied to specifc qubits, all gates')
q = qsim.DMQSimulator(3, noise_profile=None, qtrace=True, verbose=True)
q.qgate(qsim.H(),[0])
q.qgate(qsim.C(),[0,1], noise_chan=nmdl.two_qubit_dephasing(probability=0.1))

# test 07 - 2-qubit noise op - two_qubit_depolarizing
print('test 07 - adding noise at init, applied to specifc qubits, all gates')
q = qsim.DMQSimulator(3, noise_profile=None, qtrace=True, verbose=True)
q.qgate(qsim.H(),[0])
q.qgate(qsim.C(),[0,1], noise_chan=nmdl.two_qubit_depolarizing(probability=0.1))

# test0x - list noise channel/operator signatures
noise_chans_list = nmdl.noise_channel_list()
for nchanid in noise_chans_list.keys():
	print(f'{nchanid:30s}  {noise_chans_list[nchanid]}')