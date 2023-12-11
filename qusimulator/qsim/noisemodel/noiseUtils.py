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
    def __init__(self, noise_ops=None, qbit_list=None):
        self.name = ''
        self.noise_operator_sequence_applier = []
        if noise_ops is not None:
            if qbit_list is None:
                raise qsim.QSimError('ERROR: qubits list required.')
            self.add(noise_ops, qbit_list)

    def add(self, noise_ops, qbit_list):
        if type(noise_ops) is NoiseOperatorSequence:
            addition = [(op,qbit_list) for op in noise_ops]
        elif type(noise_ops) is NoiseOperator:
            addition = [(noise_ops, qbit_list)]
        else:
            raise qsim.QSimError('ERROR: NoiseOperatorSequence or NoiseOperator object expected.')
        self.noise_operator_sequence_applier.extend(addition)
        self.name = self.__name__()
    
    def extend(self, noise_op_applier_seq):
        if type(noise_op_applier_seq) is not NoiseOperatorApplierSequense:
            raise qsim.QSimError('ERROR: NoiseOperatorApplierSequense object expected')
        addition = noise_op_applier_seq.noise_operator_sequence_applier
        self.noise_operator_sequence_applier.extend(addition)
        self.name = self.__name__()

    def __name__(self):
        return ','.join([f'({oper.name},{qbits})' for oper,qbits in self.noise_operator_sequence_applier])

    def __iter__(self):
        self.it = iter(self.noise_operator_sequence_applier)
        return self.it
    def __next__(self):
        return next(self.it) 

    def __str__(self):
        return f'{self.name}'

