#!/usr/bin/env python

import qsim
import qsim.noisemodel as nmdl

print('01 All NoiseOperatorSequence')
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

print('02 All NoiseOperator only')
noise_model = {
	'noise_chan_init': nmdl.phase_flip(probability=0.2),
	'noise_chan_allgates': nmdl.depolarizing(probability=0.1),
	'noise_chan_qubits': nmdl.qNoiseChannelApplierSequense(nmdl.bit_flip(probability=0.3),[1]),
}
q = qsim.DMQSimulator(3, noise_profile=noise_model, qtrace=True, verbose=True)
q.qgate(qsim.X(),[0])
q.qnoise(noise_chan=nmdl.bit_flip(probability=0.1), qbit_list=[0,1,2], qtrace=True)
q.qgate(qsim.C(),[0,1])
q.qgate(qsim.X(),[2], noise_chan=nmdl.phase_flip(probability=0.1))
q.qgate(qsim.H(),[2])
