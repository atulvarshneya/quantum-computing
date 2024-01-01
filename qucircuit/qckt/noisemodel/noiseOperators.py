import math
import qckt.gatesutils as gutils
from qckt.noisemodel.noiseUtils import KrausOperator
import numpy as np


I = ['I',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]
X = ['X', np.matrix([[0,1],[1,0]],dtype=complex)]
Y = ['Y', np.matrix([[0,complex(0,-1)],[complex(0,1),0]],dtype=complex)]
Z = ['Z', np.matrix([[1,0],[0,-1]],dtype=complex)]
I2 = ['I2', np.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]],dtype=complex)]

# Canned noise operators (noise channels)
def bit_flip(probability=0.05):
    noise_operator = KrausOperator(
        name=f'BF({probability:.2f})',
        kraus_op=[(X,probability),(I,(1-probability))],
        nqubits=1,
        )
    return noise_operator
    # return {'name': f'BF({probability:.2f})', 'operator': [[(X,probability),(I,(1-probability))], 0.0]}


def phase_flip(probability=0.05):
    noise_operator = KrausOperator(
        name=f'PF({probability:.2f})',
        kraus_op=[(Z,probability),(I,(1-probability))],
        nqubits=1,
        )
    return noise_operator
    # return {'name': f'PF({probability:.2f})', 'operator':[[(Z,probability),(I,(1-probability))], 0.0]}


def depolarizing(probability=0.05):
    noise_operator = KrausOperator(
        name=f'Dep({probability:.2f})',
        kraus_op=[(X,probability/3.0),(Y,probability/3.0),(Z,probability/3.0),(I,(1-probability))],
        nqubits=1,
        )
    return noise_operator
    # return {'name':f'Dep({probability:.2f})', 'operator':[[(X,probability/3.0),(Y,probability/3.0),(Z,probability/3.0),(I,(1-probability))], 0.0]}


def amplitude_damping(gamma=0.05):
    AD_K1 = ['K1',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    AD_K2 = ['K2',np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    noise_operator = KrausOperator(
        name=f'AD({gamma:.2f})',
        kraus_op=[(AD_K1,1.0),(AD_K2,1.0)],
        nqubits=1,
        )
    return noise_operator
    # return {'name':f'AD({gamma:.2f})', 'operator':[[(AD_K1,1.0),(AD_K2,1.0)], 0.0]}


def phase_damping(gamma=0.05):
    PD_K0 = ['K0',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    PD_K1 = ['K1',np.matrix([[0.0,0.0],[0.0,math.sqrt(gamma)]], dtype=complex)]
    noise_operator = KrausOperator(
        name=f'PD({gamma:.2f})',
        kraus_op=[(PD_K0,1.0),(PD_K1,1.0)],
        nqubits=1,
        )
    return noise_operator
    # return {'name':f'PD({gamma:.2f})', 'operator':[[(PD_K0,1.0),(PD_K1,1.0)], 0.0]}


def pauli_channel(probx=0.05, proby=0.05, probz=0.05):
    noise_operator = KrausOperator(
        name=f'PC({probx:.2f},{proby:.2f},{probz:.2f})',
        kraus_op=[(X,probx),(Y,proby),(Z,probz),(I,(1-probx-proby-probz))],
        nqubits=1,
        )
    return noise_operator
    # return {'name': f'PC({probx:.2f},{proby:.2f},{probz:.2f})', 'operator':[[(X,probx),(Y,proby),(Z,probz),(I,(1-probx-proby-probz))], 0.0]}


def generalized_amplitude_damping(probability=0.05, gamma=0.05):
    GAD_K0 = ['K0',math.sqrt(probability)*np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    GAD_K1 = ['K1',math.sqrt(probability)*np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    GAD_K2 = ['K2',math.sqrt(1-probability)*np.matrix([[math.sqrt(1-gamma),0.0],[0.0,1.0]], dtype=complex)]
    GAD_K3 = ['K3',math.sqrt(1-probability)*np.matrix([[0.0,0.0],[math.sqrt(gamma),0.0]], dtype=complex)]
    noise_operator = KrausOperator(
        name=f'GAD({probability:.2f},{gamma:.2f})',
        kraus_op=[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)],
        nqubits=1,
        )
    return noise_operator
    # return {'name': f'GAD({probability:.2f},{gamma:.2f})', 'operator':[[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)], 0.0]}

def dummy_2qubit_kop(probability=0.05):
    noise_operator = KrausOperator(
        name=f'DUMMY-KOP({probability})',
        kraus_op=[(I2,probability),(I2,(1-probability))],
        nqubits=2,
        )
    return noise_operator

def two_qubit_dephasing(probability=0.05):
    zop = Z[1]
    iop = I[1]
    IZ = ['IZ',gutils.combine_opmatrices_par([iop,zop])]
    ZI = ['ZI',gutils.combine_opmatrices_par([zop,iop])]
    ZZ = ['ZZ',gutils.combine_opmatrices_par([zop,zop])]
    kraus_op = [
        (I2, (1-probability)),
        (IZ,probability/3.0),
        (ZI,probability/3.0),
        (ZZ,probability/3.0),
        ]
    noise_operator = KrausOperator(
        name=f'2DPH({probability})',
        kraus_op=kraus_op,
        nqubits=2,
        )
    return noise_operator

def two_qubit_depolarizing(probability=0.05):
    kraus_op = [(I2,(1-probability))]
    for op1 in [I,X,Y,Z]:
        for op2 in [I,X,Y,Z]:
            if op1[0] == 'I' and op2[0] == 'I':
                continue
            opname = f'{op1[0]}{op2[0]}'
            opmatrix = gutils.combine_opmatrices_par([op1[1],op2[1]])
            twoqbitop = [opname,opmatrix]
            kraus_op.append((twoqbitop, (probability/15.0)))
    noise_operator = KrausOperator(
        name=f'2DEP({probability})',
        kraus_op=kraus_op,
        nqubits=2,
    )
    return noise_operator


def noise_operator_list():
    return noise_op_signature

def noise_operator_lookup(noise_operator_name):
    if noise_operator_name not in noise_operators.keys():
        raise qsim.QSimError(f'{noise_operator_name} not a valid pre-prepared noise operator.')
    return noise_operators[noise_operator_name]


noise_operators = {
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

noise_op_signature = {}
for krname in noise_operators:
    fn = noise_operators[krname]
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
    noise_op_signature[krname] = signature

