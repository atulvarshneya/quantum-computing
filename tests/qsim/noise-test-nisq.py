#!/usr/bin/env python

import qsim
import qsim.noisemodel as nmdl


# print the list of canned kraus channels
noise_channels = list(nmdl.noise_operator_list().keys())
noise_channels.sort()
print(noise_channels)
print()

# test 01 - without any noise model
print('test 01 - without any noise model')
q = qsim.NISQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2])
q.qgate(qsim.H(),[2])

# test 02 - direct call to qnoise
print('test 02 - direct call to qnoise')
q = qsim.NISQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2])
q.qgate(qsim.H(),[2])

# test 03 - adding noise applied to a gate invokation
print('test 03 - adding noise applied to a gate invokation')
q = qsim.NISQSimulator(3,qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])

# test 04 - adding noise applied to all gates
print('test 04 - adding noise at init, applied to specifc qubits, all gates')
noise_model = {
	'noise_opseq_init': nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.2)),
	'noise_opseq_allgates': nmdl.NoiseOperatorSequence(nmdl.depolarizing(probability=0.1)),
	'noise_opseq_qubits': nmdl.NoiseOperatorApplierSequense(nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.3)),[1]),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])

# test 05 - a blanket test for all noise operators applied to all gates, using their default arguments
for nchanid in noise_channels:
	if nmdl.noise_operator_lookup(nchanid)().nqubits != 1:
		# print(f'skipped {nchanid}')
		continue
	print(f'test 05 - Blanket test - {nchanid}')
	krfn = nmdl.noise_operator_lookup(nchanid)
	noise_model = {
		'noise_opseq_allgates': nmdl.NoiseOperatorSequence(krfn()),
		'noise_opseq_init': None
	}
	q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
	q.qgate(qsim.X(),[0])
	q.qnoise(noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
	q.qgate(qsim.C(),[0,1])
	q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
	q.qgate(qsim.H(),[2])

# test06 - list noise channel/operator signatures
noise_chans_list = nmdl.noise_operator_list()
for nchanid in noise_chans_list.keys():
	print(f'{nchanid:30s}  {noise_chans_list[nchanid]}')