#!/usr/bin/env python

import qsim
import qsim.noisemodel as nmdl

print('01 All NoiseOperatorSequence')
noise_model = {
	'noise_opseq_init': nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.2)),
	'noise_opseq_allgates': nmdl.NoiseOperatorSequence(nmdl.depolarizing(probability=0.1)),
	'noise_opseq_qubits': nmdl.NoiseOperatorApplierSequense(nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.3)),[1]),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])

print('02 All NoiseOperator only')
noise_model = {
	'noise_opseq_init': nmdl.phase_flip(probability=0.2),
	'noise_opseq_allgates': nmdl.depolarizing(probability=0.1),
	'noise_opseq_qubits': nmdl.NoiseOperatorApplierSequense(nmdl.bit_flip(probability=0.3),[1]),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.bit_flip(probability=0.1), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.phase_flip(probability=0.1))
q.qgate(qsim.H(),[2])
