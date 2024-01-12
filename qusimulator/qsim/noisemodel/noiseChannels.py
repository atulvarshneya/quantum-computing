import math
import qsim
from qsim.noisemodel.noiseUtils import qNoiseChannel
import numpy as np

# Identity gate
I = ['I',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
X = ['X', np.matrix([[0,1],[1,0]],dtype=complex)]
Y = ['Y', np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
Z = ['Z', np.matrix([[1,0],[0,-1]],dtype=complex)]
I2 = ['I2', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]],dtype=complex)]


# Canned noise channels
def bit_flip(probability=0.05):
    noise_channel = qNoiseChannel(
        name=f'BF({probability:.2f})',
        operator_prob_set=[(qsim.X(),probability),(I,(1-probability))],
        nqubits=1,
        )
    return noise_channel


def phase_flip(probability=0.05):
    noise_channel = qNoiseChannel(
        name=f'PF({probability:.2f})',
        operator_prob_set=[(qsim.Z(),probability),(I,(1-probability))],
        nqubits=1,
        )
    return noise_channel


def depolarizing(probability=0.05):
    noise_channel = qNoiseChannel(
        name=f'Dep({probability:.2f})',
        operator_prob_set=[(qsim.X(),probability/3.0),(qsim.Y(),probability/3.0),(qsim.Z(),probability/3.0),(I,(1-probability))],
        nqubits=1,
        )
    return noise_channel


def amplitude_damping(gamma=0.05):
    AD_K1 = ['K1',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    AD_K2 = ['K2',np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    noise_channel = qNoiseChannel(
        name=f'AD({gamma:.2f})',
        operator_prob_set=[(AD_K1,1.0),(AD_K2,1.0)],
        nqubits=1,
        )
    return noise_channel


def phase_damping(gamma=0.05):
    PD_K0 = ['K0',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    PD_K1 = ['K1',np.matrix([[0.0,0.0],[0.0,math.sqrt(gamma)]], dtype=complex)]
    noise_channel = qNoiseChannel(
        name=f'PD({gamma:.2f})',
        operator_prob_set=[(PD_K0,1.0),(PD_K1,1.0)],
        nqubits=1,
        )
    return noise_channel


def pauli_channel(probx=0.05, proby=0.05, probz=0.05):
    noise_channel = qNoiseChannel(
        name=f'PC({probx:.2f},{proby:.2f},{probz:.2f})',
        operator_prob_set=[(qsim.X(),probx),(qsim.Y(),proby),(qsim.Z(),probz),(I,(1-probx-proby-probz))],
        nqubits=1,
        )
    return noise_channel


def generalized_amplitude_damping(probability=0.05, gamma=0.05):
    GAD_K0 = ['K0',math.sqrt(probability)*np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    GAD_K1 = ['K1',math.sqrt(probability)*np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    GAD_K2 = ['K2',math.sqrt(1-probability)*np.matrix([[math.sqrt(1-gamma),0.0],[0.0,1.0]], dtype=complex)]
    GAD_K3 = ['K3',math.sqrt(1-probability)*np.matrix([[0.0,0.0],[math.sqrt(gamma),0.0]], dtype=complex)]
    noise_channel = qNoiseChannel(
        name=f'GAD({probability:.2f},{gamma:.2f})',
        operator_prob_set=[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)],
        nqubits=1,
        )
    return noise_channel

def dummy_2qubit_noisechan(probability=0.05):
    noise_channel = qNoiseChannel(
        name=f'DUMMY-CHAN({probability})',
        operator_prob_set=[(I2,probability),(I2,(1-probability))],
        nqubits=2,
        )
    return noise_channel

def two_qubit_dephasing(probability=0.05):
    IZ = qsim.qcombine_par('IZ',[I,Z])
    ZI = qsim.qcombine_par('ZI',[Z,I])
    ZZ = qsim.qcombine_par('ZZ',[Z,Z])
    opprob_set = [
        (I2, (1-probability)),
        (IZ,probability/3.0),
        (ZI,probability/3.0),
        (ZZ,probability/3.0),
        ]
    noise_channel = qNoiseChannel(
        name=f'2DPH({probability})',
        operator_prob_set=opprob_set,
        nqubits=2,
        )
    return noise_channel

def two_qubit_depolarizing(probability=0.05):
    opprob_set = [(I2,(1-probability))]
    for op1 in [I,X,Y,Z]:
        for op2 in [I,X,Y,Z]:
            if op1[0] == 'I' and op2[0] == 'I':
                continue
            opname = f'{op1[0]}{op2[0]}'
            twoqbitop = qsim.qcombine_par(opname,[op1,op2])
            opprob_set.append((twoqbitop, (probability/15.0)))
    noise_channel = qNoiseChannel(
        name=f'2DEP({probability})',
        operator_prob_set=opprob_set,
        nqubits=2,
    )
    return noise_channel


def noise_channel_list():
    return noise_chan_signature

def noise_channel_lookup(noise_channel_name):
    if noise_channel_name not in noise_channels.keys():
        raise qsim.QSimError(f'{noise_channel_name} not a valid pre-prepared noise channel.')
    return noise_channels[noise_channel_name]


noise_channels = {
    'BitFlip': bit_flip,
    'PhaseFlip': phase_flip,
    'Depolarizing': depolarizing,
    'AmplitudeDamping': amplitude_damping,
    'GeneralizedAmplitudeDamping': generalized_amplitude_damping,
    'PhaseDamping': phase_damping,
    'PauliChannel': pauli_channel,
    'DUMMY-NOISECHAN': dummy_2qubit_noisechan,
    'TwoQubitDephasing': two_qubit_dephasing,
    'TwoQubitDepolarizing': two_qubit_depolarizing,
    }
noise_chan_signature = {}

for krname in noise_channels:
    fn = noise_channels[krname]
    fn_name = fn.__name__
    argcount = fn.__code__.co_argcount
    defcount = len(fn.__defaults__)
    nondefcount = argcount - defcount
    signature = f'{fn_name}('
    sep=''
    for i in range(argcount):
        argdesc = f'{fn.__code__.co_varnames[i]}'
        signature += f'{sep}{argdesc}'
        sep = ', '
        if i >= nondefcount:
            signature += f'={fn.__defaults__[i-nondefcount]}'
    signature += ')'
    noise_chan_signature[krname] = signature


if __name__ == '__main__':
    noisechan = two_qubit_depolarizing(probability=0.1)
    for chan,prob in noisechan:
        print(chan)
        print(prob)