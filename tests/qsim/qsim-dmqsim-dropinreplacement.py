import qsim
import qsim.noisemodel as nmdl

def common_qops(qc:qsim.QSimulator):
    qc.qgate(oper=qsim.H(),qbit_list=[0], noise_chan=nmdl.amplitude_damping(gamma=0.05))
    qc.qgate(qsim.C(),[0,3])
    qc.qnoise(noise_chan=nmdl.two_qubit_dephasing(probability=0.05),qbit_list=[0,1])


noise_model = {
    'noise_chan_init': nmdl.bit_flip(probability=0.05),
    'noise_chan_allgates': nmdl.depolarizing(probability=0.05)
    }
qc = qsim.DMQSimulator(4, noise_profile=noise_model, qtrace=True)
common_qops(qc)


qc = qsim.QSimulator(4, noise_profile=noise_model, qtrace=True)
common_qops(qc)

