#!/usr/bin/env python

import qsim
import qsim.noisemodel as nmdl

print('01 adding noise at init, applied to specifc qubits, all gates')
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


print('02 adding noise at init, skipping theother two')
noise_model = {
	'noise_opseq_init': nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.2)),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])


print('03 adding noise at init, other two explicitly None')
noise_model = {
	'noise_opseq_init': nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.2)),
	'noise_opseq_allgates': None,
	'noise_opseq_qubits': None,
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])



print('04 adding noise to all gates, skipping the other two')
noise_model = {
	'noise_opseq_allgates': nmdl.NoiseOperatorSequence(nmdl.depolarizing(probability=0.1)),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])



print('05 adding noise to all gates, other two explicitly None')
noise_model = {
	'noise_opseq_init': None,
	'noise_opseq_allgates': nmdl.NoiseOperatorSequence(nmdl.depolarizing(probability=0.1)),
	'noise_opseq_qubits': None,
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])



print('06 adding noise to specifc qubits, skipping other two')
noise_model = {
	'noise_opseq_qubits': nmdl.NoiseOperatorApplierSequense(nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.3)),[1]),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])



print('07 adding noise to specifc qubits, other two explicitly None')
noise_model = {
	'noise_opseq_init': None,
	'noise_opseq_allgates': None,
	'noise_opseq_qubits': nmdl.NoiseOperatorApplierSequense(nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.3)),[1]),
}
q = qsim.NISQSimulator(3, noise_model=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_op=nmdl.NoiseOperatorSequence(nmdl.bit_flip(probability=0.1)), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_op_sequence=nmdl.NoiseOperatorSequence(nmdl.phase_flip(probability=0.1)))
q.qgate(qsim.H(),[2])


