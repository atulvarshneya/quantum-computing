import math
import qckt.gatesutils as gutils
from qckt.noisemodel.noiseUtils import NoiseChannel
import numpy as np
from qsim import QSimError


I = ['I',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
X = ['X', np.matrix([[0,1],[1,0]],dtype=complex)]
Y = ['Y', np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
Z = ['Z', np.matrix([[1,0],[0,-1]],dtype=complex)]
I2 = ['I2', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]],dtype=complex)]

# Canned noise channels
def bit_flip(probability=0.05):
    noise_channel = NoiseChannel(
        name=f'BF({probability:.2f})',
        noise_chan=[(X,probability),(I,(1-probability))],
        nqubits=1,
        )
    return noise_channel


def phase_flip(probability=0.05):
    noise_channel = NoiseChannel(
        name=f'PF({probability:.2f})',
        noise_chan=[(Z,probability),(I,(1-probability))],
        nqubits=1,
        )
    return noise_channel


def depolarizing(probability=0.05):
    noise_channel = NoiseChannel(
        name=f'Dep({probability:.2f})',
        noise_chan=[(X,probability/3.0),(Y,probability/3.0),(Z,probability/3.0),(I,(1-probability))],
        nqubits=1,
        )
    return noise_channel


def amplitude_damping(gamma=0.05):
    AD_K1 = ['K1',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    AD_K2 = ['K2',np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    noise_channel = NoiseChannel(
        name=f'AD({gamma:.2f})',
        noise_chan=[(AD_K1,1.0),(AD_K2,1.0)],
        nqubits=1,
        )
    return noise_channel


def phase_damping(gamma=0.05):
    PD_K0 = ['K0',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    PD_K1 = ['K1',np.matrix([[0.0,0.0],[0.0,math.sqrt(gamma)]], dtype=complex)]
    noise_channel = NoiseChannel(
        name=f'PD({gamma:.2f})',
        noise_chan=[(PD_K0,1.0),(PD_K1,1.0)],
        nqubits=1,
        )
    return noise_channel


def pauli_channel(probx=0.05, proby=0.05, probz=0.05):
    noise_channel = NoiseChannel(
        name=f'PC({probx:.2f},{proby:.2f},{probz:.2f})',
        noise_chan=[(X,probx),(Y,proby),(Z,probz),(I,(1-probx-proby-probz))],
        nqubits=1,
        )
    return noise_channel


def generalized_amplitude_damping(probability=0.05, gamma=0.05):
    GAD_K0 = ['K0',math.sqrt(probability)*np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    GAD_K1 = ['K1',math.sqrt(probability)*np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    GAD_K2 = ['K2',math.sqrt(1-probability)*np.matrix([[math.sqrt(1-gamma),0.0],[0.0,1.0]], dtype=complex)]
    GAD_K3 = ['K3',math.sqrt(1-probability)*np.matrix([[0.0,0.0],[math.sqrt(gamma),0.0]], dtype=complex)]
    noise_channel = NoiseChannel(
        name=f'GAD({probability:.2f},{gamma:.2f})',
        noise_chan=[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)],
        nqubits=1,
        )
    return noise_channel
    # return {'name': f'GAD({probability:.2f},{gamma:.2f})', 'operator':[[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)], 0.0]}

def dummy_2qubit_chan(probability=0.05):
    noise_channel = NoiseChannel(
        name=f'DUMMY-CHAN({probability})',
        noise_chan=[(I2,probability),(I2,(1-probability))],
        nqubits=2,
        )
    return noise_channel

def two_qubit_dephasing(probability=0.05):
    zop = Z[1]
    iop = I[1]
    IZ = ['IZ',gutils.combine_opmatrices_par([iop,zop])]
    ZI = ['ZI',gutils.combine_opmatrices_par([zop,iop])]
    ZZ = ['ZZ',gutils.combine_opmatrices_par([zop,zop])]
    noise_chan = [
        (I2, (1-probability)),
        (IZ,probability/3.0),
        (ZI,probability/3.0),
        (ZZ,probability/3.0),
        ]
    noise_channel = NoiseChannel(
        name=f'2DPH({probability})',
        noise_chan=noise_chan,
        nqubits=2,
        )
    return noise_channel

def two_qubit_depolarizing(probability=0.05):
    noise_chan = [(I2,(1-probability))]
    for op1 in [I,X,Y,Z]:
        for op2 in [I,X,Y,Z]:
            if op1[0] == 'I' and op2[0] == 'I':
                continue
            opname = f'{op1[0]}{op2[0]}'
            opmatrix = gutils.combine_opmatrices_par([op1[1],op2[1]])
            twoqbitop = [opname,opmatrix]
            noise_chan.append((twoqbitop, (probability/15.0)))
    noise_channel = NoiseChannel(
        name=f'2DEP({probability})',
        noise_chan=noise_chan,
        nqubits=2,
    )
    return noise_channel


def noise_channel_list():
    return noise_chan_signature

def noise_channel_lookup(noise_channel_name):
    if noise_channel_name not in noise_channels.keys():
        raise QSimError(f'{noise_channel_name} not a valid pre-prepared noise channel.')
    return noise_channels[noise_channel_name]


noise_channels = {
    'BitFlip': bit_flip,
    'PhaseFlip': phase_flip,
    'Depolarizing': depolarizing,
    'AmplitudeDamping': amplitude_damping,
    'GeneralizedAmplitudeDamping': generalized_amplitude_damping,
    'PhaseDamping': phase_damping,
    'PauliChannel': pauli_channel,
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

