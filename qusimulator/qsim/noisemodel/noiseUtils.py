import qsim

## Noise
# noise operator (kraus operator) is specified as a sequence of pairs of list of operators. 
# NoiseOperator has three fields
#	name,
#   [ (op1,op1_prob_multiplier), (op2,op2_prob_multiplier), ...  ],
#   num_target_qubits
#
#	op is in the same format as gates, i.e., ['name', opmatrix]
#		note that mostly the opmatrix is unitary, but cases such as Amplitude Damping is not [[1.0, 0.0],[0.0, sqrt(gamma)]]
#	op_prob_multiplier gives the noise contribution by this op, i.e., = op_prob_multiplier * (op * state * op_dagger)
#
# so, in math terms, rho = op1_prob_multipier * (op1 * rho * op1_dag) + op2_prob_multiplier * (op2 * rho * op2.dag) + ...
#
#   num_target_qubits is the number of qubits this kraus operator acts on
# 

class NoiseOperator:
    def __init__(self, name, operator_prob_set,nqubits):
        self.name = name
        self.operator_prob_set = operator_prob_set
        self.nqubits = nqubits

    def __iter__(self):
        self.it = iter(self.operator_prob_set)
        return self.it
    def __next__(self):
        return next(self.it)

    def __str__(self):
        return f'name={self.name}\noperator_prob_set={self.operator_prob_set}\nnqubits={self.nqubits}'

class NoiseOperatorSequence:
    def __init__(self, *args):
        self.noise_operator_sequence = []
        for a in args:
            if a is None:
                pass
            elif type(a) is NoiseOperator:
                self.add_noise_operator(a)
            elif type(a) is NoiseOperatorSequence:
                self.add_noise_operator_sequence(a)
            else:
                raise qsim.QSimError('ERROR: Invalid argument, only NoiseOperator and NoiseOperatorSequence objects or None expected')
        self.name = self.__name__()

    def add_noise_operator_sequence(self, noise_operator_sequence):
        if noise_operator_sequence is None:
            addition = []
        elif type(noise_operator_sequence) is NoiseOperatorSequence:
            addition = noise_operator_sequence.noise_operator_sequence
        else:
            raise qsim.QSimError('ERROR: NoiseOperatorSequence object or None expected')
        self.noise_operator_sequence.extend(addition)
        self.name = self.__name__()

    def add_noise_operator(self, noise_operator):
        if noise_operator is None:
            pass
        if type(noise_operator) is  NoiseOperator:
            self.noise_operator_sequence.append(noise_operator)
        else:
            raise qsim.QSimError('ERROR: NoiseOperator object or None expected')
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
    def __init__(self, noise_ops=None, qubit_list=None):
        self.name = ''
        self.noise_operator_sequence_applier = []
        if noise_ops is not None:
            if qubit_list is None:
                raise qsim.QSimError('ERROR: qubits list required.')
            self.add(noise_ops, qubit_list)

    def add(self, noise_ops, qubit_list):
        if noise_ops is None:
            addition = []
        elif type(noise_ops) is NoiseOperatorSequence:
            addition = [(op,qubit_list) for op in noise_ops]
        elif type(noise_ops) is NoiseOperator:
            addition = [(noise_ops, qubit_list)]
        else:
            raise qsim.QSimError('ERROR: NoiseOperatorSequence, NoiseOperator object or None expected.')
        self.noise_operator_sequence_applier.extend(addition)
        self.name = self.__name__()

    def extend(self, noise_op_applier_seq):
        if noise_op_applier_seq is None:
            addition = []
        elif type(noise_op_applier_seq) is NoiseOperatorApplierSequense:
            addition = noise_op_applier_seq.noise_operator_sequence_applier
        else:
            raise qsim.QSimError('ERROR: NoiseOperatorApplierSequense object or None expected')
        self.noise_operator_sequence_applier.extend(addition)
        self.name = self.__name__()

    def new_with_filtered_qubits(self, qubit_list):
        new_noise_op_applier_seq = NoiseOperatorApplierSequense()
        for noise_operator,qblist in self.noise_operator_sequence_applier:
            filtered_qbits = [q for q in qblist if q in qubit_list]
            if len(filtered_qbits) > 0:
                new_noise_op_applier_seq.add(noise_operator,filtered_qbits)
        return new_noise_op_applier_seq

    def __name__(self):
        return ','.join([f'({oper.name},{qbits})' for oper,qbits in self.noise_operator_sequence_applier])

    def __iter__(self):
        self.it = iter(self.noise_operator_sequence_applier)
        return self.it
    def __next__(self):
        return next(self.it) 

    def __str__(self):
        return f'{self.name}'


## Noise Model fields
#   noise_opseq_init: NoiseOperatorSequence,
#   noise_opseq_qubits: NoiseOperatorApplierSequence,
#   noise_opseq_allgates: NoiseOperatorSequence,
#
class NoiseModel:
    def __init__(self, noise_opseq_init, noise_opseq_qubits, noise_opseq_allgates):
        self.noise_opseq_init = noise_opseq_init
        self.noise_opseq_qubits = noise_opseq_qubits
        self.noise_opseq_allgates = noise_opseq_allgates
    def get(self, field, defval):
        print(f'deprecated dict.get(key,default) style access, key={index}.')
        retval = defval
        if hasattr(self, field):
            retval = getattr(self, field)
        return retval
    def __getitem__(self, index):
        print(f'deprecated dict[key] style access, key={index}.')
        return self.get(index,None)
    def keys(self):
        print('deprecated dict.keys() access')
        return ['noise_opseq_init', 'noise_opseq_qubits', 'noise_opseq_allgates']


## create a NoiseOperatorApplierSequence combining all components of noise to be applied when qgate() is called with certain qubit_list
#
def consolidate_gate_noise(noise_model, gate_noise, qubit_list):
    noise_op_applier_sequence_overall = NoiseOperatorApplierSequense()

    # 1. noise on specific qubits, noise_opseq_qubits
    noise_op_applier_sequence_qubits = NoiseOperatorApplierSequense()
    if noise_model is not None:
        noise_model_qubits = noise_model.get('noise_opseq_qubits', None)
        if noise_model_qubits is not None:
            noise_op_applier_sequence_qubits = noise_model_qubits.new_with_filtered_qubits(qubit_list)
    noise_op_applier_sequence_overall.extend(noise_op_applier_sequence_qubits)
    # 2. noise on all gates, noise_opseq_allgates
    noise_op_applier_sequence_all_gates = NoiseOperatorApplierSequense()
    if noise_model is not None:
        noise_model_allgates = noise_model.get('noise_opseq_allgates', None)
        noise_op_applier_sequence_all_gates = NoiseOperatorApplierSequense(noise_ops=noise_model_allgates, qubit_list=qubit_list)
    noise_op_applier_sequence_overall.extend(noise_op_applier_sequence_all_gates)
    # 3. current gate noise
    # Qckt uses its own noise_model and passes a consolidated noise_applier at qgate invokation
    noise_op_applier_sequence_this_gate = NoiseOperatorApplierSequense()
    if gate_noise is not None:
        if type(gate_noise) is NoiseOperator:
            gate_noise_as_opseq = NoiseOperatorSequence(gate_noise)
            noise_op_applier_sequence_this_gate.add(noise_ops=gate_noise_as_opseq, qubit_list=qubit_list)
        elif type(gate_noise) is NoiseOperatorSequence:
            noise_op_applier_sequence_this_gate.add(noise_ops=gate_noise, qubit_list=qubit_list)
        elif type(gate_noise) is NoiseOperatorApplierSequense:
            # quantum computing programming frameworks (e.g., qckt) can combine any noise models into 'applier sequences'
            # new_with_filtered_qubits() is just a defensive check, it is expected to be a NO-OP if qckt works correctly
            noise_op_applier_sequence_this_gate = gate_noise.new_with_filtered_qubits(qubit_list=qubit_list)
        else:
            raise qsim.QSimError('ERROR: NoiseOperatorSequence or NoiseOperatorApplierSequense object or None expected.')
    noise_op_applier_sequence_overall.extend(noise_op_applier_sequence_this_gate)

    return noise_op_applier_sequence_overall
