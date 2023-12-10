import math
import qsim
import numpy as np

## Noise
# noise operator (kraus operator) is specified as a sequence of pairs of list of operators, and a state probability multiplier
#	= { 'name': name,
#       'operator': [[ (op1,op1_prob_multiplier), (op2,op2_prob_multiplier), ...  ], state_prob_multiplier]
#	  }
#	op is in the same format as gates, i.e., ['name', opmatrix]
#		note that mostly the opmatrix is unitary, but cases such as Amplitude Damping is not [[1.0, 0.0],[0.0, sqrt(gamma)]]
#	op_prob_multiplier gives the noise contribution by this op, i.e., = op_prob_multiplier * (op * state * op_dagger)
# state_prob_multiplier is the factor by which state is multiplied when noise is added
#	typically, state_prob_multiplier = 1 - sum(op_prob_multiplier)
#	however, in some cases, e.g., Amplitude Damping, the operator itself gives the state with noise added
#   	so in those cases the state_prob_multiplier will be 0.0; and op_orob_multiplier for those ops will be 1.0
#
# so, in math terms, rho = state_prob_multiplier * rho + op1_prob_multipier * (op1 * rho * op1_dag) + op2_prob_multiplier * (op2 * rho * op2.dag) + ...
#
#                                                        |---------------------------------------- noise_add -------------------------------------------|

class NoiseOperator:
    def __init__(self, name, operator_prob_set):
        self.name = name
        self.operator_prob_set = operator_prob_set

    def get_dict(self):
        return {'name': self.name, 'operator': self.operator_prob_set}

    def __iter__(self):
        self.it = iter(self.operator_prob_set)
        return self.it
    def __next__(self):
        return next(self.it)

    def __str__(self):
        return f'name={self.name}\noperator_prob_set={self.operator_prob_set}'

class NoiseOperatorSequence:
    def __init__(self, *args):
        self.noise_operator_sequence = []
        for a in args:
            if type(a) is NoiseOperator:
                self.noise_operator_sequence.append(a)
            elif type(a) is NoiseOperatorSequence:
                self.noise_operator_sequence.extend(a.noise_operator_sequence)
            else:
                raise qsim.QSimError('ERROR: Invalid argument, only NoiseOperator and NoiseOperatorSequence objects expected')
        self.name = self.__name__()

    def get_dict(self):
        return {'operator_sequence': self.noise_operator_sequence}

    def add_noise_operator_sequence(self, noise_operator_sequence):
        if type(noise_operator_sequence) is not NoiseOperatorSequence:
            raise qsim.QSimError('ERROR: NoiseOperatorSequence object expected')
        self.noise_operator_sequence.extend(noise_operator_sequence.noise_operator_sequence)
        self.name = self.__name__()

    def add_noise_operator(self, noise_operator):
        if type(noise_operator) is not NoiseOperator:
            raise qsim.QSimError('ERROR: NoiseOperator object expected')
        self.noise_operator_sequence.append(noise_operator)
        self.name = self.__name__()

    def __iter__(self):
        self.it = iter(self.noise_operator_sequence)
        return self.it
    def __next__(self):
        return next(self.it)

    def __name__(self):
        return ','.join([oper.name for oper in self.noise_operator_sequence])

    def __str__(self):
        return self.name

class NoiseOperatorApplierSequense:
    def __init__(self, noise_operator_sequence, qbit_list):
        if type(noise_operator_sequence) is not NoiseOperatorSequence:
            raise qsim.QSimError('ERROR: NoiseOperatorSequence object expected.')
        self.noise_operator_sequence = noise_operator_sequence.noise_operator_sequence
        self.qbit_list = qbit_list
        self.name = ','.join([oper.name for oper in self.noise_operator_sequence])
        self.noise_operator_sequence_applier = [(op,self.qbit_list) for op in self.noise_operator_sequence]

    def get_dict(self):
        return {'name': self.name, 'operator_sequence': self.noise_operator_sequence, 'qbit_list': self.qbit_list}

    def __iter__(self):
        self.it = iter(self.noise_operator_sequence_applier)
        return self.it
    def __next__(self):
        return next(self.it) 

    def __str__(self):
        return f'{self.name}, {self.qbit_list}'


I = ['I',np.matrix([[1.0,0.0],[0.0,1.0]],dtype=complex)]


# Canned noise operators (noise channels)
def bit_flip(probability=0.05):
    noise_operator = NoiseOperator(
        name=f'BF({probability:.2f})',
        operator_prob_set=[(qsim.X(),probability),(I,(1-probability))],
        )
    # return noise_operator
    return {'name': f'BF({probability:.2f})', 'operator': [[(qsim.X(),probability),(I,(1-probability))], 0.0]}


def phase_flip(probability=0.05):
    noise_operator = NoiseOperator(
        name=f'PF({probability:.2f})',
        operator_prob_set=[(qsim.Z(),probability),(I,(1-probability))],
        )
    # return noise_operator
    return {'name': f'PF({probability:.2f})', 'operator':[[(qsim.Z(),probability),(I,(1-probability))], 0.0]}


def depolarizing(probability=0.05):
    noise_operator = NoiseOperator(
        name=f'Dep({probability:.2f})',
        operator_prob_set=[(qsim.X(),probability/3.0),(qsim.Y(),probability/3.0),(qsim.Z(),probability/3.0),(I,(1-probability))],
        )
    # return noise_operator
    return {'name':f'Dep({probability:.2f})', 'operator':[[(qsim.X(),probability/3.0),(qsim.Y(),probability/3.0),(qsim.Z(),probability/3.0),(I,(1-probability))], 0.0]}


def amplitude_damping(gamma=0.05):
    AD_K1 = ['K1',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    AD_K2 = ['K2',np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    noise_operator = NoiseOperator(
        name=f'AD({gamma:.2f})',
        operator_prob_set=[(AD_K1,1.0),(AD_K2,1.0)],
        )
    # return noise_operator
    return {'name':f'AD({gamma:.2f})', 'operator':[[(AD_K1,1.0),(AD_K2,1.0)], 0.0]}


def phase_damping(gamma=0.05):
    PD_K0 = ['K0',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    PD_K1 = ['K1',np.matrix([[0.0,0.0],[0.0,math.sqrt(gamma)]], dtype=complex)]
    noise_operator = NoiseOperator(
        name=f'PD({gamma:.2f})',
        operator_prob_set=[(PD_K0,1.0),(PD_K1,1.0)],
        )
    # return noise_operator
    return {'name':f'PD({gamma:.2f})', 'operator':[[(PD_K0,1.0),(PD_K1,1.0)], 0.0]}


def pauli_channel(probx=0.05, proby=0.05, probz=0.05):
    noise_operator = NoiseOperator(
        name=f'PC({probx:.2f},{proby:.2f},{probz:.2f})',
        operator_prob_set=[(qsim.X(),probx),(qsim.Y(),proby),(qsim.Z(),probz),(I,(1-probx-proby-probz))],
        )
    # return noise_operator
    return {'name': f'PC({probx:.2f},{proby:.2f},{probz:.2f})', 'operator':[[(qsim.X(),probx),(qsim.Y(),proby),(qsim.Z(),probz),(I,(1-probx-proby-probz))], 0.0]}


def generalized_amplitude_damping(probability=0.05, gamma=0.05):
    GAD_K0 = ['K0',math.sqrt(probability)*np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    GAD_K1 = ['K1',math.sqrt(probability)*np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    GAD_K2 = ['K2',math.sqrt(1-probability)*np.matrix([[math.sqrt(1-gamma),0.0],[0.0,1.0]], dtype=complex)]
    GAD_K3 = ['K3',math.sqrt(1-probability)*np.matrix([[0.0,0.0],[math.sqrt(gamma),0.0]], dtype=complex)]
    noise_operator = NoiseOperator(
        name=f'GAD({probability:.2f},{gamma:.2f})',
        operator_prob_set=[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)],
        )
    # return noise_operator
    return {'name': f'GAD({probability:.2f},{gamma:.2f})', 'operator':[[(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)], 0.0]}


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


if __name__ == '__main__':
    nop1 = bit_flip(0.2)
    for op,prob in nop1:
        print(op)
    nop2 = phase_flip(0.3)
    nop3 = bit_flip(0.4)
    noseq1 = NoiseOperatorSequence(nop1)
    noseq2 = NoiseOperatorSequence(nop2,nop3)
    noseq = NoiseOperatorSequence(noseq1, noseq2)
    for nop in noseq:
        print('----------------------------')
        print(nop)